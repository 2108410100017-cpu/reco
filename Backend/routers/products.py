# backend/routers/products.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
import pandas as pd
import torch
import shutil
import os
from datetime import datetime
from typing import Optional
from fastapi import Request
from config import IMAGE_DIR, BUSINESS_PRODUCTS_PATH
from models import RecommendRequest, BusinessProduct
# FIX: Only import the function, not the global variables
from database import get_product_by_id 

router = APIRouter(tags=["products"])
@router.get("/test")
def test_endpoint():
    """A simple test to see if the products router is working."""
    return {"status": "ok"}

@router.post("/recommend")
def recommend(req: RecommendRequest):
    # Import global variables inside the function
    from database import metadata, id_list, image_embs

    import clip
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, _ = clip.load("ViT-B/32", device=device)

    # --- FIX: Encode the user's text query ---
    tokens = clip.tokenize([req.query]).to(device)
    with torch.no_grad():
        text_embedding = model.encode_text(tokens)
        text_embedding = text_embedding / text_embedding.norm(dim=-1, keepdim=True)
    text_embedding = text_embedding.cpu()

    # --- Calculate similarity between text and all image embeddings ---
    sims = (text_embedding @ image_embs.T).squeeze(0)
    top_k = sims.topk(req.top_k)

    results = []
    for score, idx in zip(top_k.values, top_k.indices):
        pid = id_list[idx]
        
        if pid not in metadata.index:
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
# In backend/routers/products.py

# Add this new endpoint to the file
@router.get("/similar/{product_id}")
def find_similar_products(product_id: int, top_k: int = 10):
    """
    Finds products with the most similar image embeddings to the given product_id.
    """
    # Import necessary variables inside the function
    from database import metadata, image_embs, id_list
    
    # --- Step 1: Check if the product exists ---
    if product_id not in metadata.index:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
    
    # --- Step 2: Get the embedding of the target product ---
    # We need to find the index of the product_id in our id_list
    try:
        target_index = id_list.index(product_id)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Product ID {product_id} not found in trained embeddings.")

    target_embedding = image_embs[target_index]
    
    # --- Step 3: Calculate similarity with all products ---
    # Cosine similarity: (A @ B.T) gives us similarity scores
    similarity_scores = (target_embedding @ image_embs.T).squeeze(0)
    
    # --- Step 4: Get the top-k most similar products ---
    # We use `torch.topk` to find the indices of the highest scores
    top_scores, top_indices = similarity_scores.topk(top_k)
    
    # --- Step 5: Format the results ---
    results = []
    for score, idx in zip(top_scores, top_indices):
        # The index corresponds to an ID in our id_list
        similar_pid = id_list[idx]
        
        # Skip the product itself if it appears in the results
        if similar_pid == product_id:
            continue
            
        # Get product details from the metadata
        row = metadata.loc[similar_pid]
        price = float(row.get("price", 0.0))
        if pd.isna(price): price = 0.0
        
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
            "score": float(score), # This is the true similarity score
            "image_url": image_url
        })

    return results


@router.get("/debug/product/{product_id}")
def debug_product(product_id: int, request: Request):
    try:
        metadata = request.app.state.product_metadata

        row = metadata.loc[metadata['id'] == product_id]
        if row.empty:
            return {"error": f"Product {product_id} not found in metadata"}

        item = row.iloc[0]

        return {
            "id": int(item['id']),
            "name": item.get('name', None),
            "price": float(item.get('price', 0.0)),
            "image_url": f"/images/{item['id']}.jpg"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))