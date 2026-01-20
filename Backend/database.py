# backend/database.py
import os
import pandas as pd
import torch
import sys
from config import (
    EMB_PATH, META_PATH, BUSINESS_PRODUCTS_PATH, 
    IMAGE_DIR, RETRAIN_SCRIPT_PATH, ADD_PRICES_SCRIPT_PATH
)

# Global variables to hold our data in memory
metadata = None
business_products = None
emb = None
image_embs = None
text_embs = None
id_list = None

def load_combined_metadata():
    """Loads the combined metadata from both original and business products."""
    global metadata
    
    print("--- Loading Combined Metadata ---")
    
    if not os.path.exists(META_PATH):
        print(f"ERROR: {META_PATH} not found!")
        raise RuntimeError("metadata.csv missing")
    original_metadata = pd.read_csv(META_PATH)
    print(f"Loaded {len(original_metadata)} products from {META_PATH}")
    
    combined = original_metadata
    if os.path.exists(BUSINESS_PRODUCTS_PATH):
        business_products_df = pd.read_csv(BUSINESS_PRODUCTS_PATH)
        print(f"Loaded {len(business_products_df)} products from {BUSINESS_PRODUCTS_PATH}")
        combined = pd.concat([original_metadata, business_products_df], ignore_index=True)
        print(f"Combined total: {len(combined)} products")
    else:
        print(f"{BUSINESS_PRODUCTS_PATH} not found. Using only original metadata.")
        
    metadata = combined.set_index('id', drop=False)
    print("--- Metadata Loading Complete ---")

def initialize_data():
    """Initializes all data on server startup."""
    global metadata, business_products, emb, image_embs, text_embs, id_list

    # Load metadata
    load_combined_metadata()

    # Initialize business products file if it doesn't exist
    if not os.path.exists(BUSINESS_PRODUCTS_PATH):
        pd.DataFrame(columns=['id', 'business_id', 'name', 'description', 'price', 'image_path', 'added_date']).to_csv(BUSINESS_PRODUCTS_PATH, index=False)

    # Load embeddings
    if not os.path.exists(EMB_PATH):
        raise RuntimeError("embeddings.pt missing. Run retrain first.")
    
    emb = torch.load(EMB_PATH)
    image_embs = emb['image_embeddings']
    text_embs = emb['text_embeddings']
    image_embs = image_embs / image_embs.norm(dim=-1, keepdim=True)

    if 'valid_ids' in emb:
        id_list = emb['valid_ids']
    else:
        print("Warning: 'valid_ids' not found in embeddings.pt. Falling back to metadata.csv. Please retrain.")
        id_list = metadata['id'].tolist()

def get_product_by_id(product_id: int):
    """Finds a product by its ID, checking in-memory first, then business products file."""
    global metadata, BUSINESS_PRODUCTS_PATH
    
    if product_id in metadata.index:
        return metadata.loc[product_id]
    
    # Fallback to file
    business_df = pd.read_csv(BUSINESS_PRODUCTS_PATH)
    product_rows = business_df[business_df['id'] == product_id]
    if not product_rows.empty:
        return product_rows.iloc[0]
        
    return None