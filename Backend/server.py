import sys

import os
import torch
import subprocess

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
RETRAIN_SCRIPT_PATH = os.path.join(TRAIN_DIR, "retrain.py")

app = FastAPI()


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    # Get the path to the python executable that is running this server
    python_executable = sys.executable

    # Check if the script exists
    if not os.path.exists(RETRAIN_SCRIPT_PATH):
        raise HTTPException(status_code=404, detail=f"Retrain script not found at {RETRAIN_SCRIPT_PATH}")

    try:
        # Use the specific python_executable to run the script
        # This ensures it uses the same environment with torch, pandas, etc.
        result = subprocess.run(
            [python_executable, RETRAIN_SCRIPT_PATH], 
            check=True, 
            capture_output=True, 
            text=True, 
            cwd=TRAIN_DIR
        )
        
        print("Retrain stdout:", result.stdout)
        
        return {"status": "started", "message": "Retraining process initiated successfully."}

    except subprocess.CalledProcessError as e:
        # This will catch errors if the script itself fails
        print(f"Error during retrain: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"Retraining script failed: {e.stderr}")
    except FileNotFoundError:
        # This catches the case where sys.executable itself is not found (very rare)
        raise HTTPException(status_code=500, detail="Python executable not found.")

# ---------- Health Check -----------

@app.get("/health")
def health():
    return {"status": "ok"}
