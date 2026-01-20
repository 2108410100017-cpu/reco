import sys
import os
import torch
import subprocess
import pandas as pd
import uuid
import shutil
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_DIR = os.path.join(BASE_DIR, "../Training")

EMB_PATH = os.path.join(TRAIN_DIR, "embeddings.pt")
META_PATH = os.path.join(TRAIN_DIR, "metadata.csv")
STYLES_PATH = os.path.join(TRAIN_DIR, "styles.csv")
IMAGE_DIR = os.path.join(TRAIN_DIR, "images")
RETRAIN_SCRIPT_PATH = os.path.join(TRAIN_DIR, "retrain.py")
ADD_PRICES_SCRIPT_PATH = os.path.join(TRAIN_DIR, "add_prices.py")
BUSINESS_PRODUCTS_PATH = os.path.join(TRAIN_DIR, "business_products.csv")
COMBINED_METADATA_PATH = os.path.join(TRAIN_DIR, "combined_metadata.csv")

# Mount static files
if os.path.exists(IMAGE_DIR):
    app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

# FIX: Add these new Pydantic models at the top with the others
class CartItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    image_url: str

class Cart(BaseModel):
    items: list[CartItem]
    total_price: float

# --- FIX: Add this global variable for cart storage ---
# For a real app, this would be in a database and tied to a user ID
carts = {}
DEFAULT_CART_ID = "default_cart"

# FIX: This is the CORRECT and ONLY definition of this function.
def load_combined_metadata():
    """Loads the combined metadata from both original and business products."""
    global metadata
    
    print("--- Loading Combined Metadata ---")
    
    # Load the original metadata
    if not os.path.exists(META_PATH):
        print(f"ERROR: {META_PATH} not found!")
        raise RuntimeError("metadata.csv missing")
    original_metadata = pd.read_csv(META_PATH)
    print(f"Loaded {len(original_metadata)} products from {META_PATH}")
    
    # Load business products
    combined = original_metadata
    if os.path.exists(BUSINESS_PRODUCTS_PATH):
        business_products = pd.read_csv(BUSINESS_PRODUCTS_PATH)
        print(f"Loaded {len(business_products)} products from {BUSINESS_PRODUCTS_PATH}")
        # Combine them
        combined = pd.concat([original_metadata, business_products], ignore_index=True)
        print(f"Combined total: {len(combined)} products")
    else:
        print(f"{BUSINESS_PRODUCTS_PATH} not found. Using only original metadata.")
        
    # Set the index for fast lookups and update the global variable
    metadata = combined.set_index('id', drop=False)
    print("--- Metadata Loading Complete ---")


# FIX: This is the new startup logic. It calls the function above.
# --------- Load Metadata ---------
load_combined_metadata()

# Load styles if available
styles = pd.read_csv(STYLES_PATH, on_bad_lines='skip', quotechar='"', engine='python') if os.path.exists(STYLES_PATH) else None

# Initialize business products file if it doesn't exist
if not os.path.exists(BUSINESS_PRODUCTS_PATH):
    business_products = pd.DataFrame(columns=['id', 'business_id', 'name', 'description', 'price', 'image_path', 'added_date'])
    business_products.to_csv(BUSINESS_PRODUCTS_PATH, index=False)
else:
    business_products = pd.read_csv(BUSINESS_PRODUCTS_PATH)

# Load embeddings
if not os.path.exists(EMB_PATH):
    raise RuntimeError("embeddings.pt missing. Run retrain first.")

emb = torch.load(EMB_PATH)
image_embs = emb['image_embeddings']
text_embs = emb['text_embeddings']  # optional

# Normalize embeddings
image_embs = image_embs / image_embs.norm(dim=-1, keepdim=True)

# Map index → product id
# This ensures id_list and image_embs always have the same length
if 'valid_ids' in emb:
    id_list = emb['valid_ids']
else:
    # Fallback for old embedding files that don't have valid_ids
    print("Warning: 'valid_ids' not found in embeddings.pt. Falling back to metadata.csv. Please retrain.")
    id_list = metadata['id'].tolist()

    
# Pydantic models
class RecommendRequest(BaseModel):
    query: str
    top_k: int = 10

class BusinessProduct(BaseModel):
    business_id: str
    name: str
    description: str = ""
    price: float

# API Endpoints
@app.post("/recommend")
def recommend(req: RecommendRequest):
    import clip
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    tokens = clip.tokenize([req.query]).to(device)
    with torch.no_grad():
        q = model.encode_text(tokens)
        q = q / q.norm(dim=-1, keepdim=True)
    q = q.cpu()

    sims = (q @ image_embs.T).squeeze(0)
    top_k = sims.topk(req.top_k)

    results = []
    for score, idx in zip(top_k.values, top_k.indices):
        pid = id_list[idx]
        
        # --- DEFENSIVE FIX: Check if the product exists in metadata ---
        # Using .loc is faster with an indexed DataFrame
        if pid not in metadata.index:
            print(f"Warning: Product ID {pid} found in embeddings but not in metadata. Skipping.")
            continue # Skip this product and move to the next one
        
        row = metadata.loc[pid]
        
        # Ensure price is always included, with a default value if it doesn't exist
        price = row.get("price", 0.0)
        if pd.isna(price):  # Handle NaN values
            price = 0.0
        
        # Determine the image URL
        if 'business_id' in row and pd.notna(row['business_id']):
            path = row['image_path']
            if path.startswith('images/'):
                image_url = f"/{path}"
            else:
                image_url = f"/images/{path}"
        else:
            image_url = f"/images/{pid}.jpg"
            
        results.append({
            "id": int(pid),
            "name": row.get("name", ""),
            "price": float(price),
            "score": float(score),
            "image_url": image_url
        })

    return JSONResponse(results)

@app.get("/image/{pid}")
def get_image(pid: str):
    # First check if this is a business product using the indexed metadata
    if int(pid) in metadata.index:
        row = metadata.loc[int(pid)]
        if 'business_id' in row and pd.notna(row['business_id']):
            image_filename = row['image_path']
            path = os.path.join(IMAGE_DIR, image_filename)
            if os.path.exists(path):
                return FileResponse(path)

    # Fallback for regular products or if business product image not found
    path = os.path.join(IMAGE_DIR, f"{pid}.jpg")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(path)

@app.get("/latest")
def get_latest(n: int = 50):
    try:
        print("--- Fetching Latest Products ---")
        
        # --- FIX: Use the same loading logic for consistency ---
        # Reload business products to get the latest data
        business_products = pd.read_csv(BUSINESS_PRODUCTS_PATH)
        print(f"Found {len(business_products)} business products.")
        
        # Create a copy of the in-memory metadata to avoid modifying the original
        # We reset the index to ensure a clean concat operation
        metadata_copy = metadata.reset_index(drop=True).copy()
        
        # Add a placeholder added_date for regular products
        metadata_copy['added_date'] = '1970-01-01 00:00:00'
        print(f"Found {len(metadata_copy)} original products.")
        
        # Combine regular metadata and business products
        combined_products = pd.concat([metadata_copy, business_products], ignore_index=True)
        print(f"Combined total products: {len(combined_products)}")
        
        # Sort by added_date in descending order (newest first)
        # Business products will be at the top
        combined_products = combined_products.sort_values(by='added_date', ascending=False)
        
        # Get the top 'n' items
        latest_df = combined_products.head(n)
        
        # --- Robust Image URL Creation ---
        def get_clean_image_url(row):
            try:
                # Check if it's a business product
                if 'business_id' in row and pd.notna(row['business_id']):
                    path = row['image_path']
                    if path.startswith('images/'):
                        return f"/{path}"
                    else:
                        return f"/images/{path}"
                else:
                    # It's a regular product
                    return f"/images/{int(row['id'])}.jpg"
            except Exception as e:
                print(f"Error creating image URL for row {row.get('id', 'unknown')}: {e}")
                return "/images/placeholder.jpg" # Return a placeholder on error

        # Apply the function to create the image_url column
        latest_df['image_url'] = latest_df.apply(get_clean_image_url, axis=1)

        # Convert to a list of dictionaries for the JSON response
        result = latest_df.fillna('').to_dict(orient="records")
        print(f"Returning {len(result)} latest products.")
        print("--- Latest Products Fetch Complete ---")
        
        return result

    except Exception as e:
        # Catch any unexpected errors and log them
        print(f"Error in /latest endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching latest products: {str(e)}")


# --- FIX: Add the missing Cart API Endpoints ---
@app.post("/cart/add", response_model=dict)
def add_to_cart(product_id: int, quantity: int = 1):
    """Add a product to the cart."""
    cart_id = DEFAULT_CART_ID
    if cart_id not in carts:
        carts[cart_id] = {"items": [], "total_price": 0.0}

    cart = carts[cart_id]
    
    product = None
    image_url = ""

    # --- STEP 1: Try to find the product in the in-memory metadata ---
    if product_id in metadata.index:
        print(f"Found product {product_id} in in-memory metadata.")
        product = metadata.loc[product_id]
        
        # Determine the image URL
        if 'business_id' in product and pd.notna(product['business_id']):
            path = product['image_path']
            if path.startswith('images/'):
                image_url = f"/{path}"
            else:
                image_url = f"/images/{path}"
        else:
            image_url = f"/images/{product_id}.jpg"
    
    else:
        # --- STEP 2: If not in memory, look directly in the business products file ---
        print(f"Product {product_id} not in memory. Checking business_products.csv...")
        try:
            business_df = pd.read_csv(BUSINESS_PRODUCTS_PATH)
            business_product_rows = business_df[business_df['id'] == product_id]
            
            if not business_product_rows.empty:
                print(f"Found product {product_id} in business_products.csv.")
                product = business_product_rows.iloc[0]
                
                # Construct the image URL for the business product
                path = product['image_path']
                if path.startswith('images/'):
                    image_url = f"/{path}"
                else:
                    image_url = f"/images/{path}"
            else:
                # --- STEP 3: If still not found, it's a 404 ---
                raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found anywhere.")
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Business products file is missing.")
        except Exception as e:
            print(f"Error reading business products file: {e}")
            raise HTTPException(status_code=500, detail="An error occurred while looking up the product.")

    # Add the item to the cart
    # Check if item is already in cart
    for item in cart["items"]:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            break
    else:
        # If not in cart, add it
        cart["items"].append({
            "product_id": int(product_id),
            "name": product["name"],
            "price": float(product["price"]),
            "quantity": quantity,
            "image_url": image_url
        })

    # Recalculate total price
    cart["total_price"] = sum(item["price"] * item["quantity"] for item in cart["items"])
    
    return {"status": "success", "message": f"Added {product['name']} to cart."}


@app.get("/cart", response_model=Cart)
def get_cart():
    """Get the current cart contents."""
    cart_id = DEFAULT_CART_ID
    if cart_id not in carts:
        return {"items": [], "total_price": 0.0}
    return carts[cart_id]


@app.delete("/cart/item/{product_id}", response_model=dict)
def remove_from_cart(product_id: int):
    """Remove an item from the cart."""
    cart_id = DEFAULT_CART_ID
    if cart_id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart = carts[cart_id]
    initial_length = len(cart["items"])
    cart["items"] = [item for item in cart["items"] if item["product_id"] != product_id]
    
    if len(cart["items"]) == initial_length:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    # Recalculate total price
    cart["total_price"] = sum(item["price"] * item["quantity"] for item in cart["items"])
    
    return {"status": "success", "message": "Item removed from cart."}


@app.post("/cart/clear", response_model=dict)
def clear_cart():
    """Clear all items from the cart."""
    cart_id = DEFAULT_CART_ID
    carts[cart_id] = {"items": [], "total_price": 0.0}
    return {"status": "success", "message": "Cart cleared."}


@app.get("/debug/product/{product_id}")
def debug_product(product_id: int):
    """Debug endpoint to check if a product exists in the server's data."""
    global metadata, business_products
    
    # Check if the product exists in the in-memory metadata
    if product_id in metadata.index:
        product_info = metadata.loc[product_id].to_dict()
        return {
            "status": "found_in_memory",
            "product_id": product_id,
            "source": "in-memory metadata DataFrame",
            "product_info": product_info
        }
    
    # If not in memory, check the original files
    original_metadata = pd.read_csv(META_PATH)
    if product_id in original_metadata['id'].values:
        product_info = original_metadata[original_metadata['id'] == product_id].iloc[0].to_dict()
        return {
            "status": "found_in_file",
            "product_id": product_id,
            "source": "original metadata.csv file",
            "product_info": product_info,
            "message": "Product exists in file but was not loaded into memory. Try restarting the server."
        }
        
    # Check business products file
    if os.path.exists(BUSINESS_PRODUCTS_PATH):
        business_products_df = pd.read_csv(BUSINESS_PRODUCTS_PATH)
        if product_id in business_products_df['id'].values:
            product_info = business_products_df[business_products_df['id'] == product_id].iloc[0].to_dict()
            return {
                "status": "found_in_business_file",
                "product_id": product_id,
                "source": "business_products.csv file",
                "product_info": product_info,
                "message": "Product exists in business file but was not loaded into memory. Try restarting the server."
            }

    # If we get here, it's truly not found anywhere
    return {
        "status": "not_found",
        "product_id": product_id,
        "message": f"Product ID {product_id} was not found in any data source."
    }


@app.post("/retrain")
def retrain():
    global business_products, emb, image_embs, text_embs, id_list
    
    python_executable = sys.executable
    
    # Reload business products to get the latest data
    business_products = pd.read_csv(BUSINESS_PRODUCTS_PATH)
    
    # Create a copy of the original metadata (not the in-memory one)
    original_metadata = pd.read_csv(META_PATH)
    original_metadata['added_date'] = '1970-01-01 00:00:00'
    
    # Combine the datasets
    combined_products = pd.concat([original_metadata, business_products], ignore_index=True)
    
    # Save the combined products to a CSV file for retraining
    combined_products.to_csv(COMBINED_METADATA_PATH, index=False)
    
    if not os.path.exists(RETRAIN_SCRIPT_PATH):
        raise HTTPException(status_code=404, detail=f"Retrain script not found at {RETRAIN_SCRIPT_PATH}")
    
    try:
        # Pass the combined metadata path to the retrain script
        result = subprocess.run(
            [python_executable, RETRAIN_SCRIPT_PATH, "--metadata", COMBINED_METADATA_PATH], 
            check=True, 
            capture_output=True, 
            text=True, 
            cwd=TRAIN_DIR
        )
        
        print("Retrain stdout:", result.stdout)
        
        # --- CRITICAL FIX: Use our new function to reload metadata ---
        load_combined_metadata()
        
        # Reload embeddings AND id_list from the file
        emb = torch.load(EMB_PATH)
        image_embs = emb['image_embeddings']
        text_embs = emb['text_embeddings']
        image_embs = image_embs / image_embs.norm(dim=-1, keepdim=True)
        
        # Load the matching id_list
        if 'valid_ids' in emb:
            id_list = emb['valid_ids']
        else:
            raise RuntimeError("Retrained embeddings.pt is missing 'valid_ids'. This should not happen.")
        
        return {"status": "success", "message": f"Retraining completed. Model now has {len(id_list)} products."}
    
    except subprocess.CalledProcessError as e:
        print(f"Error during retrain: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"Retraining script failed: {e.stderr}")

@app.post("/add-prices")
def add_prices():
    """Add price information to all products in the metadata"""
    python_executable = sys.executable
    
    if not os.path.exists(ADD_PRICES_SCRIPT_PATH):
        raise HTTPException(status_code=404, detail=f"Add prices script not found at {ADD_PRICES_SCRIPT_PATH}")
    
    try:
        result = subprocess.run(
            [python_executable, ADD_PRICES_SCRIPT_PATH], 
            check=True, 
            capture_output=True, 
            text=True, 
            cwd=TRAIN_DIR
        )
        
        # FIX: Reload the COMBINED metadata after adding prices
        load_combined_metadata()
        
        return {"status": "success", "message": "Prices added to all products"}
    
    except subprocess.CalledProcessError as e:
        print(f"Error adding prices: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"Failed to add prices: {e.stderr}")

@app.post("/business/add-product")
async def add_business_product(
    business_id: str = Form(...),
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    image: UploadFile = File(...)
):
    # Declare global variables at the beginning of the function
    global business_products

    # Reload business products to get the latest data
    business_products = pd.read_csv(BUSINESS_PRODUCTS_PATH)
    
    # --- Start of Unique ID Generation Logic ---
    # Find the starting point for the new ID
    max_metadata_id = int(metadata['id'].max()) if len(metadata) > 0 else 0
    max_business_id = int(business_products['id'].max()) if len(business_products) > 0 else 0
    new_id = max(max_metadata_id, max_business_id) + 1

    # Keep looping until we find an ID that doesn't exist in either dataset
    while (new_id in metadata.index) or (new_id in business_products['id'].values):
        print(f"ID {new_id} already exists. Trying next one...")
        new_id += 1
    # --- End of Unique ID Generation Logic ---

    # Save the uploaded image
    image_filename = f"{new_id}.jpg"
    image_path = os.path.join(IMAGE_DIR, image_filename)
    
    try:
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving image: {str(e)}")
    
    # Add the new product to business_products
    new_product = pd.DataFrame([{
        'id': int(new_id),
        'business_id': business_id,
        'name': name,
        'description': description,
        'price': float(price),
        'image_path': image_filename,  # Just store the filename, not the full path
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    # Use pd.concat instead of append (which is deprecated)
    business_products = pd.concat([business_products, new_product], ignore_index=True)
    business_products.to_csv(BUSINESS_PRODUCTS_PATH, index=False)
    
    # Return with explicitly converted types to ensure JSON serialization works
    return {
        "id": int(new_id), 
        "status": "success", 
        "message": f"Product added successfully with unique ID: {new_id}"
    }

@app.get("/health")
def health():
    return {"status": "ok"}