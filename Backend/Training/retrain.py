import os
import torch
import clip
import pandas as pd
from PIL import Image
from tqdm import tqdm
import argparse

def main():
    # --- 1. Parse Command-Line Arguments ---
    parser = argparse.ArgumentParser(description='Retrain the recommendation model on the full dataset.')
    parser.add_argument('--metadata', type=str, required=True, help='Path to the combined metadata CSV file.')
    args = parser.parse_args()

    # --- 2. Setup Paths and Device ---
    # The directory where the script is running (should be the Training folder)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMAGE_DIR = os.path.join(BASE_DIR, "images")
    EMB_PATH = os.path.join(BASE_DIR, "embeddings.pt")
    
    # Get the metadata path from the arguments
    META_PATH = args.metadata

    # Check if the metadata file exists
    if not os.path.exists(META_PATH):
        print(f"Error: Metadata file not found at {META_PATH}")
        return

    # --- 3. Load Model and Data ---
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    model, preprocess = clip.load("ViT-B/32", device=device)

    print(f"Loading metadata from: {META_PATH}")
    metadata = pd.read_csv(META_PATH)
    print(f"Found {len(metadata)} products to process.")

    # --- 4. Process Each Product and Create Embeddings ---
    image_embeddings = []
    text_embeddings = []
    valid_ids = [] # Keep track of IDs that were successfully processed

    for index, row in tqdm(metadata.iterrows(), total=len(metadata), desc="Processing products"):
        product_id = row['id']
        
        # --- Determine the correct image path ---
        # Check if it's a business product (has 'image_path' and 'business_id')
        if 'business_id' in row and pd.notna(row['business_id']) and 'image_path' in row and pd.notna(row['image_path']):
            image_path = os.path.join(IMAGE_DIR, row['image_path'])
        else:
            # It's a regular product, construct the path from the ID
            image_path = os.path.join(IMAGE_DIR, f"{product_id}.jpg")

        # --- Process the image and text ---
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert("RGB")
            image_tensor = preprocess(image).unsqueeze(0).to(device)

            # Get the product name for text encoding
            product_name = row.get('name', '') # Use 'name' column, fallback to empty string
            
            # Encode image and text
            with torch.no_grad():
                image_emb = model.encode_image(image_tensor)
                text_emb = model.encode_text(clip.tokenize([product_name]).to(device))

            image_embeddings.append(image_emb.cpu())
            text_embeddings.append(text_emb.cpu())
            valid_ids.append(product_id)

        except FileNotFoundError:
            print(f"Warning: Image not found for product ID {product_id} at {image_path}. Skipping.")
        except Exception as e:
            print(f"Warning: Failed to process product ID {product_id}. Error: {e}. Skipping.")

    if not image_embeddings:
        print("Error: No products were successfully processed. Embeddings file not created.")
        return

    # --- 5. Combine and Save Embeddings ---
    print("Combining embeddings...")
    image_embeddings = torch.cat(image_embeddings, dim=0)
    text_embeddings = torch.cat(text_embeddings, dim=0)

    print(f"Saving {len(image_embeddings)} embeddings to: {EMB_PATH}")
    torch.save({
        'image_embeddings': image_embeddings,
        'text_embeddings': text_embeddings,
        'valid_ids': valid_ids # Optional: save list of IDs that correspond to embeddings
    }, EMB_PATH)

    print("Retraining completed successfully!")


if __name__ == "__main__":
    main()