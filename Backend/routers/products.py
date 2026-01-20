# backend/routers/products.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
import pandas as pd
import torch
import shutil
import os
from datetime import datetime
from typing import Optional

from config import IMAGE_DIR, BUSINESS_PRODUCTS_PATH
from models import RecommendRequest, BusinessProduct
# FIX: Only import the function, not the global variables
from database import get_product_by_id 

router = APIRouter(tags=["products"])

@router.post("/recommend")
def recommend(req: RecommendRequest):
    # FIX: Import global variables inside the function
    from database import metadata, id_list, image_embs

    import clip
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, _ = clip.load("ViT-B/32", device=device)

    tokens = clip.tokenize([req.query]).to(device)
    with torch.no_grad():
        q = model.encode_text(tokens)
        q = q / q.norm(dim=-1, keepdim=True)
    q = q.cpu()

    # Now image_embs is guaranteed to be initialized
    sims = (q @ image_embs.T).squeeze(0)
    top_k = sims.topk(req.top_k)

    results = []
    for score, idx in zip(top_k.values, top_k.indices):
        pid = id_list[idx]
        
        if pid not in metadata.index:
            print(f"Warning: Product ID {pid} found in embeddings but not in metadata. Skipping.")
            continue
        
        row = metadata.loc[pid]
        price = float(row.get("price", 0.0))
        if pd.isna(price): price = 0.0
        
        image_url = ""
        if 'business_id' in row and pd.notna(row['business_id']):
            path = row['image_path']
            image_url = f"/{path}" if path.startswith('images/') else f"/images/{path}"
        else:
            image_url = f"/images/{pid}.jpg"
            
        results.append({
            "id": int(pid), "name": row.get("name", ""), "price": price,
            "score": float(score), "image_url": image_url
        })

    return JSONResponse(results)

@router.get("/latest")
def get_latest(n: int = 50):
    # FIX: Import metadata inside the function
    from database import metadata
    
    try:
        business_df = pd.read_csv(BUSINESS_PRODUCTS_PATH)
        # Now metadata is guaranteed to be initialized
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
            except Exception as e:
                print(f"Error creating image URL for row {row.get('id', 'unknown')}: {e}")
                return "/images/placeholder.jpg"

        latest_df['image_url'] = latest_df.apply(get_clean_image_url, axis=1)
        return latest_df.fillna('').to_dict(orient="records")
    except Exception as e:
        print(f"Error in /latest endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/image/{pid}")
def get_image(pid: str):
    # FIX: Import the function inside the function
    from database import get_product_by_id
    
    product = get_product_by_id(int(pid))
    if product and 'business_id' in product and pd.notna(product['business_id']):
        image_filename = product['image_path']
        path = os.path.join(IMAGE_DIR, image_filename)
        if os.path.exists(path):
            return FileResponse(path)
    
    path = os.path.join(IMAGE_DIR, f"{pid}.jpg")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(path)

@router.post("/business/add-product")
async def add_business_product(
    business_id: str = Form(...), name: str = Form(...), 
    description: str = Form(""), price: float = Form(...), 
    image: UploadFile = File(...)
):
    # FIX: Import metadata inside the function
    from database import metadata
    
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
        raise HTTPException(status_code=500, detail=f"Error saving image: {str(e)}")
    
    new_product = pd.DataFrame([{
        'id': int(new_id), 'business_id': business_id, 'name': name,
        'description': description, 'price': float(price),
        'image_path': image_filename, 'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    updated_df = pd.concat([business_df, new_product], ignore_index=True)
    updated_df.to_csv(BUSINESS_PRODUCTS_PATH, index=False)
    
    return {"id": int(new_id), "status": "success", "message": f"Product added with ID: {new_id}"}