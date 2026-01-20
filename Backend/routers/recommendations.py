# backend/routers/recommendations.py
from fastapi import APIRouter
from database import metadata
import pandas as pd

router = APIRouter(tags=["recommendations"])

@router.get("/random")
def get_random_products(n: int = 12):
    """
    Fetches a specified number of random products from the combined dataset.
    """
    print("--- /random endpoint called ---")
    
    # Import metadata inside the function
    from database import metadata
    
    print(f"Length of in-memory metadata DataFrame: {len(metadata)}")
    if len(metadata) == 0:
        print("!!! METADATA IS EMPTY. This is the problem. !!!")
        return []
    
    # Reset the index before sampling
    metadata_for_sample = metadata.reset_index(drop=True).copy()
    
    # Now, sample from the temporary DataFrame
    random_products_df = metadata_for_sample.sample(n=min(n, len(metadata_for_sample)))
    
    print(f"Length of sampled DataFrame: {len(random_products_df)}")

    def get_clean_image_url(row):
        try:
            if 'business_id' in row and pd.notna(row['business_id']):
                path = row['image_path']
                return f"/{path}" if path.startswith('images/') else f"/images/{path}"
            return f"/images/{int(row['id'])}.jpg"
        except Exception as e:
            print(f"Error creating image URL for row {row.get('id', 'unknown')}: {e}")
            return "/images/placeholder.jpg"

    random_products_df['image_url'] = random_products_df.apply(get_clean_image_url, axis=1)
    
    # Convert to a list of dictionaries
    result = random_products_df.fillna('').to_dict(orient="records")
    
    print(f"Length of final result list: {len(result)}")
    print("--- /random endpoint finished ---")
    
    return result

# In backend/routers/recommendations.py

@router.get("/similar/{product_id}")
def find_similar_products(product_id: int, top_k: int = 10):
    """
    Finds products with the most similar image embeddings to the given product_id.
    """
    print(f"--- /similar/{product_id} endpoint called ---")
    
    # Import necessary variables inside the function
    from database import metadata, image_embs, id_list
    
    print(f"Looking for Product ID: {product_id}")
    print(f"Total products in metadata: {len(metadata)}")
    print(f"Total embeddings in id_list: {len(id_list)}")
    
    # --- Step 1: Check if the product exists ---
    if product_id not in metadata.index:
        print(f"!!! ERROR: Product ID {product_id} not found in metadata DataFrame.")
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
    
    # --- Step 2: Get the embedding of the target product ---
    try:
        target_index = id_list.index(product_id)
        print(f"SUCCESS: Found product {product_id} at index {target_index} in id_list.")
    except ValueError:
        print(f"!!! ERROR: Product ID {product_id} not found in trained embeddings (id_list).")
        raise HTTPException(status_code=404, detail=f"Product ID {product_id} not found in trained embeddings.")

    target_embedding = image_embs[target_index]
    
    # --- Step 3: Calculate similarity with all products ---
    similarity_scores = (target_embedding @ image_embs.T).squeeze(0)
    
    # --- Step 4: Get the top-k most similar products ---
    top_scores, top_indices = similarity_scores.topk(top_k)
    
    print(f"Found {len(top_indices)} similar products.")
    
    # --- Step 5: Format the results ---
    results = []
    for score, idx in zip(top_scores, top_indices):
        similar_pid = id_list[idx]
        
        # Skip the product itself if it appears in the results
        if similar_pid == product_id:
            print(f"Skipping self: {similar_pid}")
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
            "score": float(score),
            "image_url": image_url
        })

    print(f"Returning {len(results)} results after filtering.")
    print("--- /similar/{product_id} endpoint finished ---")
    
    return results