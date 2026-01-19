import os
import torch
import clip
import pandas as pd
from PIL import Image
from tqdm import tqdm

IMAGE_DIR = "images"
CSV_PATH = "styles.csv"
EMB_PATH = "embeddings.pt"
# META_PATH = "metadata.csv"
BATCH_SIZE = 64
BAD_ROWS_LOG = "bad_rows.log"
MAX_ROWS = 2000  # read only first 2000 rows

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

import argparse
import os

# Add argument parsing at the beginning of your retrain.py
parser = argparse.ArgumentParser(description='Retrain the recommendation model')
parser.add_argument('--metadata', type=str, default='metadata.csv', help='Path to the metadata file')
args = parser.parse_args()

# Then use args.metadata instead of a hardcoded path
META_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.metadata)

# The rest of your retrain.py code...


def encode_image(path):
    img = Image.open(path).convert("RGB")
    img = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        e = model.encode_image(img)
        e = e / e.norm(dim=-1, keepdim=True)
    return e.cpu()

def encode_text(text):
    tokens = clip.tokenize([text]).to(device)
    with torch.no_grad():
        e = model.encode_text(tokens)
        e = e / e.norm(dim=-1, keepdim=True)
    return e.cpu()

def incremental_retrain():
    # ---------------------------
    # Read CSV safely (up to MAX_ROWS)
    # ---------------------------
    bad_rows = []
    def log_bad_line(line_num, line):
        bad_rows.append((line_num, line))

    try:
        new_df = pd.read_csv(
            CSV_PATH,
            on_bad_lines='skip',  # skip malformed rows
            quotechar='"',        # handle commas inside quoted text
            nrows=MAX_ROWS        # read only first 2000 rows
        )
    except Exception as e:
        print("Error reading CSV:", e)
        return

    # ---------------------------
    # Compare with existing metadata
    # ---------------------------
    if os.path.exists(META_PATH):
        old = pd.read_csv(META_PATH)
        new_df = new_df[~new_df['id'].astype(str).isin(old['id'].astype(str))]

    # ---------------------------
    # Add image paths and filter existing files
    # ---------------------------
    new_df['image_path'] = new_df['id'].astype(str).apply(lambda x: os.path.join(IMAGE_DIR, f"{x}.jpg"))
    new_df = new_df[new_df['image_path'].apply(os.path.exists)]
    print("NEW SAMPLES:", len(new_df))

    if len(new_df) == 0:
        print("No new data to embed")
        return

    # ---------------------------
    # Encode images and text
    # ---------------------------
    img_embs, txt_embs = [], []
    meta_rows = []

    for _, r in tqdm(new_df.iterrows(), total=len(new_df)):
        try:
            img_embs.append(encode_image(r['image_path']))
            txt_embs.append(encode_text(r.get('productDisplayName', "")))
            meta_rows.append(r)
        except Exception as e:
            print(f"Failed to encode row {r['id']}: {e}")
            continue

    img_embs = torch.cat(img_embs, dim=0)
    txt_embs = torch.cat(txt_embs, dim=0)
    new_meta = pd.DataFrame(meta_rows)

    # ---------------------------
    # Merge with existing embeddings
    # ---------------------------
    if os.path.exists(EMB_PATH):
        emb = torch.load(EMB_PATH)
        img_embs = torch.cat([emb['image_embeddings'], img_embs], dim=0)
        txt_embs = torch.cat([emb['text_embeddings'], txt_embs], dim=0)

    torch.save({
        'image_embeddings': img_embs,
        'text_embeddings': txt_embs
    }, EMB_PATH)

    # ---------------------------
    # Merge metadata
    # ---------------------------
    if os.path.exists(META_PATH):
        old = pd.read_csv(META_PATH)
        pd.concat([old, new_meta]).to_csv(META_PATH, index=False)
    else:
        new_meta.to_csv(META_PATH, index=False)

    # ---------------------------
    # Log any bad rows if found
    # ---------------------------
    if bad_rows:
        with open(BAD_ROWS_LOG, 'w', encoding='utf-8') as f:
            for line_num, line in bad_rows:
                f.write(f"{line_num}: {line}\n")
        print(f"Skipped {len(bad_rows)} malformed rows. See {BAD_ROWS_LOG} for details.")

    print("Incremental retrain complete")

if __name__ == "__main__":
    incremental_retrain()
