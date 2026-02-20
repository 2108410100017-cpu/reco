from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, FileResponse
import pandas as pd
import torch
import shutil
import os
from datetime import datetime
from typing import Optional

from config import IMAGE_DIR, BUSINESS_PRODUCTS_PATH
from models import RecommendRequest, BusinessProduct
from database import get_product_by_id 
import math

router = APIRouter(tags=["products"])


# -------------------------------
# User Identity Helper (NEW)
# -------------------------------
def get_user_id(request: Request):
    """
    Consistent identity handling:
    - Frontend logged user via header
    - Fallback guest
    """
    user_id = request.headers.get("X-User-ID")
    return user_id if user_id else "guest"


# -------------------------------
# Health Test Endpoint
# -------------------------------
@router.get("/test")
def test_endpoint():
    return {"status": "ok"}


# -------------------------------
# TEXT RECOMMENDATION
# -------------------------------
from database import metadata, id_list, image_embs
import math
from fastapi.responses import JSONResponse
from datetime import datetime
import torch
import clip
import pandas as pd
import math
# Force embeddings to CPU (important for Render)
image_embs = image_embs.cpu()

# Load CLIP model once (NOT inside route)
device = "cuda" if torch.cuda.is_available() else "cpu"
model, _ = clip.load("ViT-B/32", device=device)
model.eval()
@router.post("/recommend")
def recommend(req: RecommendRequest):
    try:
        # Encode query
        tokens = clip.tokenize([req.query]).to(device)

        with torch.no_grad():
            text_embedding = model.encode_text(tokens)
            text_embedding = text_embedding / text_embedding.norm(dim=-1, keepdim=True)

        text_embedding = text_embedding.cpu()

        # Similarity
        sims = (text_embedding @ image_embs.T).squeeze(0)

        # Safe top_k
        k = min(req.top_k, sims.shape[0])
        top_k = sims.topk(k)

        results = []
        dates = []

        for score, idx in zip(top_k.values, top_k.indices):
            idx = idx.item()  # FIX tensor indexing
            pid = id_list[idx]

            if pid not in metadata.index:
                continue

            row = metadata.loc[pid]

            price = float(row.get("price", 0.0))
            if pd.isna(price):
                price = 0.0

            # Safe date parsing
            added_date = pd.to_datetime(
                row.get("added_date", "1970-01-01"),
                errors="coerce"
            )

            if pd.isna(added_date):
                added_date = pd.to_datetime("1970-01-01")

            dates.append(added_date)

            # Image URL logic
            if "business_id" in row and pd.notna(row["business_id"]):
                path = row.get("image_path", "")
                if path.startswith("images/"):
                    image_url = f"/{path}"
                else:
                    image_url = f"/images/{path}"
            else:
                image_url = f"/images/{pid}.jpg"

            results.append({
                "id": int(pid),
                "name": row.get("name", ""),
                "price": price,
                "score": float(score),
                "image_url": image_url,
                "added_date": added_date
            })

        # -------- HYBRID RANKING --------
        if results:
            max_sim = max(r["score"] for r in results)
            min_date = min(dates)
            max_date = max(dates)

            for r in results:
                sim = r["score"]

                # Freshness score
                if max_date != min_date:
                    freshness = (
                        (r["added_date"] - min_date).total_seconds()
                        / (max_date - min_date).total_seconds()
                    )
                else:
                    freshness = 0.0

                # Hybrid weighting
                if max_sim != 0 and abs(max_sim - sim) <= 0.02 * max_sim:
                    final_score = 0.85 * sim + 0.15 * freshness
                else:
                    final_score = sim

                if math.isnan(final_score):
                    final_score = 0.0

                r["final_score"] = float(final_score)

            results.sort(key=lambda x: x["final_score"], reverse=True)

        # Convert datetime → string for JSON
        for r in results:
            r["added_date"] = r["added_date"].strftime("%Y-%m-%d %H:%M:%S")

        return JSONResponse(content=results)

    except Exception as e:
        import traceback
        print("ERROR:", traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# -------------------------------
# LATEST PRODUCTS
# -------------------------------
@router.get("/latest")
def get_latest(n: int = 50):
    from database import metadata

    try:
        business_df = pd.read_csv(BUSINESS_PRODUCTS_PATH)

        metadata_copy = metadata.reset_index(drop=True).copy()
        metadata_copy['added_date'] = '1970-01-01 00:00:00'

        combined = pd.concat([metadata_copy, business_df], ignore_index=True)
        combined = combined.sort_values(by='added_date', ascending=False)

        latest_df = combined.head(n)

        def get_clean_image_url(row):
            try:
                if 'business_id' in row and pd.notna(row['business_id']):
                    path = row['image_path']
                    return f"/{path}" if path.startswith('images/') else f"/images/{path}"
                return f"/images/{int(row['id'])}.jpg"
            except:
                return "/images/placeholder.jpg"

        latest_df['image_url'] = latest_df.apply(get_clean_image_url, axis=1)

        return latest_df.fillna('').to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# IMAGE FETCH
# -------------------------------
@router.get("/image/{pid}")
def get_image(pid: str):
    from database import get_product_by_id

    product = get_product_by_id(int(pid))

    if product is not None and 'business_id' in product and pd.notna(product['business_id']):
        image_filename = product['image_path']
        path = os.path.join(IMAGE_DIR, image_filename)

        if os.path.exists(path):
            return FileResponse(path)

    path = os.path.join(IMAGE_DIR, f"{pid}.jpg")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(path)


# -------------------------------
# ADD BUSINESS PRODUCT (IDENTITY FIXED)
# -------------------------------
@router.post("/business/add-product")
async def add_business_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    image: UploadFile = File(...),
):
    from database import metadata

    # NEW: get user identity
    business_id = get_user_id(request)

    business_df = pd.read_csv(BUSINESS_PRODUCTS_PATH)

    max_id = int(metadata['id'].max()) if len(metadata) > 0 else 0
    max_business_id = int(business_df['id'].max()) if len(business_df) > 0 else 0

    new_id = max(max_id, max_business_id) + 1

    image_filename = f"{new_id}.jpg"
    image_path = os.path.join(IMAGE_DIR, image_filename)

    try:
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    new_product = pd.DataFrame([{
        'id': int(new_id),
        'business_id': business_id,
        'name': name,
        'description': description,
        'price': float(price),
        'image_path': image_filename,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    updated_df = pd.concat([business_df, new_product], ignore_index=True)
    updated_df.to_csv(BUSINESS_PRODUCTS_PATH, index=False)

    return {
        "id": int(new_id),
        "status": "success",
        "message": f"Product added with ID: {new_id}",
        "business_id": business_id
    }


# -------------------------------
# SIMILAR PRODUCTS
# -------------------------------
@router.get("/similar/{product_id}")
def find_similar_products(product_id: int, top_k: int = 10):

    from database import metadata, image_embs, id_list

    if product_id not in metadata.index:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        target_index = id_list.index(product_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Embedding not found")

    target_embedding = image_embs[target_index]

    similarity_scores = (target_embedding @ image_embs.T).squeeze(0)
    top_scores, top_indices = similarity_scores.topk(top_k)

    results = []

    for score, idx in zip(top_scores, top_indices):
        similar_pid = id_list[idx]

        if similar_pid == product_id:
            continue

        row = metadata.loc[similar_pid]

        price = float(row.get("price", 0.0))
        if pd.isna(price):
            price = 0.0

        image_url = ""
        if 'business_id' in row and pd.notna(row['business_id']):
            path = row['image_path']
            image_url = f"/{path}" if path.startswith('images/') else f"/images/{path}"
        else:
            image_url = f"/images/{similar_pid}.jpg"

        results.append({
            "id": int(similar_pid),
            "name": row.get("name", ""),
            "price": price,
            "score": float(score),
            "image_url": image_url
        })

    return results
