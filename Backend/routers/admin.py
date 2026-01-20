# backend/routers/admin.py
from fastapi import APIRouter, HTTPException
import subprocess
import sys
import pandas as pd
import torch
from config import (
    RETRAIN_SCRIPT_PATH, ADD_PRICES_SCRIPT_PATH, 
    TRAIN_DIR, COMBINED_METADATA_PATH, BUSINESS_PRODUCTS_PATH, META_PATH, EMB_PATH # FIX: Import EMB_PATH directly
)
# FIX: Only import the function
from database import load_combined_metadata

router = APIRouter(tags=["admin"])

@router.post("/retrain")
def retrain():
    # FIX: Import global variables inside the function
    from database import emb, image_embs, text_embs, id_list
    
    python_executable = sys.executable
    business_df = pd.read_csv(BUSINESS_PRODUCTS_PATH)
    original_df = pd.read_csv(META_PATH)
    original_df['added_date'] = '1970-01-01 00:00:00'
    
    combined = pd.concat([original_df, business_df], ignore_index=True)
    combined.to_csv(COMBINED_METADATA_PATH, index=False)
    
    try:
        result = subprocess.run(
            [python_executable, RETRAIN_SCRIPT_PATH, "--metadata", COMBINED_METADATA_PATH], 
            check=True, capture_output=True, text=True, cwd=TRAIN_DIR
        )
        
        load_combined_metadata() # Reload metadata into memory
        
        # Re-import to get the updated values
        from database import emb, image_embs, text_embs, id_list
        
        # FIX: Use EMB_PATH directly, not config.EMB_PATH
        emb = torch.load(EMB_PATH)
        image_embs = emb['image_embeddings']
        text_embs = emb['text_embeddings']
        image_embs = image_embs / image_embs.norm(dim=-1, keepdim=True)
        
        if 'valid_ids' in emb:
            id_list = emb['valid_ids']
        else:
            raise RuntimeError("Retrained embeddings.pt is missing 'valid_ids'.")
        
        return {"status": "success", "message": f"Retraining completed. Model has {len(id_list)} products."}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Retraining failed: {e.stderr}")

@router.post("/add-prices")
def add_prices():
    python_executable = sys.executable
    try:
        subprocess.run(
            [python_executable, ADD_PRICES_SCRIPT_PATH], 
            check=True, capture_output=True, text=True, cwd=TRAIN_DIR
        )
        load_combined_metadata()
        return {"status": "success", "message": "Prices added to all products"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Failed to add prices: {e.stderr}")

@router.get("/health")
def health():
    return {"status": "ok"}