import os
import torch
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_DIR = os.path.join(BASE_DIR, "../Training")

EMB_PATH = os.path.join(TRAIN_DIR, "embeddings.pt")
META_PATH = os.path.join(TRAIN_DIR, "metadata.csv")
STYLES_PATH = os.path.join(TRAIN_DIR, "styles.csv")
IMAGE_DIR = os.path.join(TRAIN_DIR, "images")

app = FastAPI()

# attach images directory
if os.path.exists(IMAGE_DIR):
    app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

# --------- Load Metadata ---------
if not os.path.exists(META_PATH):
    raise RuntimeError("metadata.csv missing")

metadata = pd.read_csv(META_PATH)

styles = pd.read_csv(STYLES_PATH, on_bad_lines='skip', quotechar='"', engine='python') if os.path.exists(STYLES_PATH) else None

# --------- Load Embeddings ---------
if not os.path.exists(EMB_PATH):
    raise RuntimeError("embeddings.pt missing. Run retrain first.")

emb = torch.load(EMB_PATH)
image_embs = emb['image_embeddings']
text_embs = emb['text_embeddings']  # optional

# simple normalize
image_embs = image_embs / image_embs.norm(dim=-1, keepdim=True)

# map index → product id
id_list = metadata['id'].tolist()


# ---------- Recommendation API -----------

class RecommendRequest(BaseModel):
    query: str
    top_k: int = 10


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
        row = metadata[metadata['id'] == pid].iloc[0]
        results.append({
            "id": int(pid),
            "name": row.get("name", ""),
            "score": float(score),
            "image_url": f"/images/{pid}.jpg"
        })

    return JSONResponse(results)


# ---------- Serve Images -----------

@app.get("/image/{pid}")
def get_image(pid: int):
    path = os.path.join(IMAGE_DIR, f"{pid}.jpg")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(path)


# ---------- Get Latest Metadata -----------

@app.get("/latest")
def get_latest(n: int = 50):
    df = metadata.tail(n)
    return df.to_dict(orient="records")


# ---------- Trigger Retrain -----------

@app.post("/retrain")
def retrain():
    os.system(f"python retrain.py")
    return {"status": "started"}


# ---------- Health Check -----------

@app.get("/health")
def health():
    return {"status": "ok"}
