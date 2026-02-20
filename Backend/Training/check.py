import torch
import pandas as pd

emb = torch.load(r"C:\Users\EDGE-02\Documents\Anurag\reco\Training\embeddings.pt")
meta = pd.read_csv(r"C:\Users\EDGE-02\Documents\Anurag\reco\Training\combined_metadata.csv")

print("Embeddings:", len(emb['image_embeddings']))
print("Valid IDs:", len(emb['valid_ids']))
print("Metadata:", len(meta))
