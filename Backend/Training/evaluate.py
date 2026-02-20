import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# LOAD EMBEDDINGS
# =========================
EMB_PATH = r"C:\Users\EDGE-02\Documents\Anurag\reco\Training\embeddings.pt"

emb = torch.load(EMB_PATH, map_location="cpu")

img_emb = emb["image_embeddings"].numpy()
txt_emb = emb["text_embeddings"].numpy()

# Fuse embeddings (recommended)
catalog_emb = (img_emb + txt_emb) / 2


# =========================
# SIMILARITY FUNCTION
# =========================
def get_similar_products(idx, top_k=10):
    sims = cosine_similarity([catalog_emb[idx]], catalog_emb)[0]
    top_idx = sims.argsort()[::-1][1:top_k+1]
    return top_idx, sims[top_idx]


# =========================
# BASIC QUALITY CHECK
# =========================
def evaluate_basic():

    avg_top_sim = []

    for i in range(50):  # test first 50 items
        _, scores = get_similar_products(i)
        avg_top_sim.append(scores.mean())

    print("\n===== Quick Embedding Quality =====")
    print("Average Similarity:", np.mean(avg_top_sim))
    print("Max Similarity:", np.max(avg_top_sim))
    print("Min Similarity:", np.min(avg_top_sim))

    if np.mean(avg_top_sim) > 0.45:
        print("Excellent embedding quality")
    elif np.mean(avg_top_sim) > 0.3:
        print("Good recommendation quality")
    else:
        print("Needs improvement")


if __name__ == "__main__":
    evaluate_basic()
