import os
import pandas as pd
import torch
import clip
from PIL import Image
from tqdm import tqdm

# ==========================
# CONFIG
# ==========================
IMAGE_DIR = "images"
CSV_PATH = "styles.csv"
OUTPUT_EMB_PATH = "embeddings.pt"
OUTPUT_META_PATH = "metadata.csv"
SAMPLE_SIZE = 1500

# ==========================
# LOAD DATA
# ==========================
df = pd.read_csv(CSV_PATH, on_bad_lines="skip")

df = df.dropna(subset=["id"])
df["id"] = df["id"].astype(str)

df["image_path"] = df["id"].apply(
    lambda x: os.path.join(IMAGE_DIR, f"{x}.jpg")
)

df = df[df["image_path"].apply(os.path.exists)]

df = df.head(SAMPLE_SIZE)

print(f"Training on {len(df)} products")

# ==========================
# LOAD MODEL
# ==========================
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", device)

model, preprocess = clip.load("ViT-B/32", device=device)
model.eval()  # IMPORTANT

# ==========================
# EMBEDDING STORAGE
# ==========================
image_embeddings = []
text_embeddings = []
metadata_rows = []

# ==========================
# ENCODING LOOP
# ==========================
for _, row in tqdm(df.iterrows(), total=len(df), desc="Encoding"):

    img_path = row["image_path"]
    name = str(row.get("productDisplayName", ""))

    try:
        img = Image.open(img_path).convert("RGB")
    except Exception as e:
        print(f"Skipping {img_path} due to error: {e}")
        continue

    img_tensor = preprocess(img).unsqueeze(0).to(device)
    text_tokens = clip.tokenize([name]).to(device)

    with torch.no_grad():
        img_emb = model.encode_image(img_tensor)
        txt_emb = model.encode_text(text_tokens)

        img_emb = img_emb / img_emb.norm(dim=-1, keepdim=True)
        txt_emb = txt_emb / txt_emb.norm(dim=-1, keepdim=True)

    image_embeddings.append(img_emb.cpu())
    text_embeddings.append(txt_emb.cpu())

    metadata_rows.append({
        "id": row["id"],
        "name": name,
        "image_path": img_path
    })

# ==========================
# SAVE OUTPUTS
# ==========================
if len(image_embeddings) == 0:
    raise ValueError("No embeddings generated!")

image_embeddings = torch.cat(image_embeddings, dim=0)
text_embeddings = torch.cat(text_embeddings, dim=0)
metadata_df = pd.DataFrame(metadata_rows)

torch.save({
    "image_embeddings": image_embeddings,
    "text_embeddings": text_embeddings
}, OUTPUT_EMB_PATH)

metadata_df.to_csv(OUTPUT_META_PATH, index=False)

print("=== Training Completed ===")
print(f"Embeddings shape: {image_embeddings.shape}")
print(f"Embeddings saved to: {OUTPUT_EMB_PATH}")
print(f"Metadata saved to: {OUTPUT_META_PATH}")
