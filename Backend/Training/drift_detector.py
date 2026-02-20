import torch
import pandas as pd
from sklearn.metrics import kl_divergence
import os 
META_PATH = "metadata.csv"
EMB_PATH = "embeddings.pt"

def compute_embedding_drift():
    emb = torch.load(EMB_PATH)['image_embeddings']
    centroid = emb.mean(dim=0)
    prev = torch.load("emb_prev.pt")['image_embeddings'].mean(dim=0) if os.path.exists("emb_prev.pt") else None

    if prev is None:
        torch.save({'image_embeddings': emb}, "emb_prev.pt")
        return 0

    drift = torch.norm(centroid - prev).item()
    torch.save({'image_embeddings': emb}, "emb_prev.pt")
    return drift

def compute_attribute_drift():
    df = pd.read_csv(META_PATH)
    new_dist = df['gender'].value_counts(normalize=True)
    old = pd.read_csv("meta_prev.csv") if os.path.exists("meta_prev.csv") else None

    if old is None: 
        df.to_csv("meta_prev.csv", index=False)
        return 0

    old_dist = old['gender'].value_counts(normalize=True)
    drift = (new_dist - old_dist).abs().sum()
    df.to_csv("meta_prev.csv", index=False)
    return drift

if __name__ == "__main__":
    emb_d = compute_embedding_drift()
    attr_d = compute_attribute_drift()
    print("embedding drift:", emb_d)
    print("attribute drift:", attr_d)
