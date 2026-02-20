import torch
import clip
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import logging
import traceback

# ✅ IMPORT PATHS FROM CONFIG
from config import EMB_PATH, META_PATH

# ==========================
# LOGGING
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ==========================
# LOAD DATA (FIXED PATHS)
# ==========================
try:
    logging.info(f"Loading embeddings from: {EMB_PATH}")
    emb = torch.load(EMB_PATH, map_location="cpu")

    logging.info(f"Loading metadata from: {META_PATH}")
    meta = pd.read_csv(META_PATH)

except Exception as e:
    logging.error("Failed loading embeddings or metadata")
    logging.error(traceback.format_exc())
    raise e

# ==========================
# VALIDATE EMBEDDINGS
# ==========================
required_keys = ["image_embeddings", "text_embeddings"]

for key in required_keys:
    if key not in emb:
        raise ValueError(f"Missing required key in embeddings file: {key}")

img_emb = emb["image_embeddings"]
txt_emb = emb["text_embeddings"]

# fuse embeddings
catalog_emb = (img_emb + txt_emb) / 2
catalog_emb = catalog_emb.numpy()

logging.info(f"Loaded {catalog_emb.shape[0]} embeddings successfully")

# ==========================
# LOAD CLIP MODEL
# ==========================
device = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"Device: {device}")

model, preprocess = clip.load("ViT-B/32", device=device)

# ==========================
# ATTRIBUTE FILTERING
# ==========================
colors = [
    "black","white","red","blue","green",
    "yellow","brown","pink","grey","navy","maroon"
]

categories = [
    "shirt","tshirt","top","jeans","dress",
    "sneakers","shoes","jacket","hoodie","kurta"
]

def filter_metadata(query: str):
    q = query.lower()
    filtered = meta.copy()

    found_colors = [c for c in colors if c in q]
    found_cats = [c for c in categories if c in q]

    if found_colors:
        for c in found_colors:
            filtered = filtered[
                filtered['name'].str.contains(c, case=False, na=False)
            ]

    if found_cats:
        for c in found_cats:
            filtered = filtered[
                filtered['name'].str.contains(c, case=False, na=False)
            ]

    if filtered.empty:
        logging.warning("Attribute filter returned no result. Falling back to full data.")
        return meta, False

    return filtered, True


# ==========================
# MAIN RECOMMEND FUNCTION
# ==========================
def recommend(query: str, top_k=5):
    try:
        logging.info(f"Query received: {query}")

        # Apply attribute filtering
        filtered_meta, attr_ok = filter_metadata(query)
        idx = filtered_meta.index.tolist()

        if not idx:
            logging.warning("No valid indices found after filtering.")
            return pd.DataFrame()

        # Encode query using CLIP
        text_tokens = clip.tokenize([query]).to(device)

        with torch.no_grad():
            txt_vec = model.encode_text(text_tokens)
            txt_vec = txt_vec / txt_vec.norm(dim=-1, keepdim=True)

        query_vec = txt_vec.cpu().numpy()

        # Subset embeddings
        subset_emb = catalog_emb[idx]

        # Compute similarity
        sims = cosine_similarity(query_vec, subset_emb)[0]
        top_idx = sims.argsort()[::-1][:top_k]

        results = filtered_meta.iloc[top_idx].copy()
        results["score"] = sims[top_idx]

        if not attr_ok:
            logging.info("Results returned using fallback (no attribute match).")

        return results

    except Exception:
        logging.error("Exception occurred inside recommend()")
        logging.error(traceback.format_exc())
        return pd.DataFrame()


# ==========================
# LOCAL TEST
# ==========================
if __name__ == "__main__":
    q = "navy blue check shirt"
    output = recommend(q, top_k=5)
    print(output)