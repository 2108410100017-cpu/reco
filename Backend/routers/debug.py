# backend/routers/debug.py
from fastapi import APIRouter
import pandas as pd
import os
from config import META_PATH, BUSINESS_PRODUCTS_PATH, EMB_PATH
# FIX: Only import the function
from database import get_product_by_id

router = APIRouter(tags=["debug"])

@router.get("/product/{product_id}")
def debug_product(product_id: int):
    # FIX: Import the function inside the function
    from database import get_product_by_id
    
    product = get_product_by_id(product_id)
    if product:
        return {"status": "found", "product_id": product_id, "source": "database lookup"}
    
    # Fallback checks if the function returns None
    original_df = pd.read_csv(META_PATH)
    if product_id in original_df['id'].values:
        return {"status": "found_in_file", "product_id": product_id, "source": "metadata.csv"}
        
    if os.path.exists(BUSINESS_PRODUCTS_PATH):
        business_df = pd.read_csv(BUSINESS_PRODUCTS_PATH)
        if product_id in business_df['id'].values:
            return {"status": "found_in_business_file", "product_id": product_id, "source": "business_products.csv"}

    return {"status": "not_found", "product_id": product_id, "message": "Product not found anywhere."}