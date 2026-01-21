# backend/database.py
import os
import pandas as pd
import torch
import sys
from config import (
    EMB_PATH, META_PATH, BUSINESS_PRODUCTS_PATH, 
    IMAGE_DIR, RETRAIN_SCRIPT_PATH, ADD_PRICES_SCRIPT_PATH
)
import logging # Add this import at the top
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    
    # Load original metadata with id as integer
    original_metadata = pd.read_csv(META_PATH, dtype={'id': int})
    print(f"Loaded {len(original_metadata)} products from {META_PATH}")
    
    combined = original_metadata
    if os.path.exists(BUSINESS_PRODUCTS_PATH):
        # Load business products with id as integer
        business_products_df = pd.read_csv(BUSINESS_PRODUCTS_PATH, dtype={'id': int})
        print(f"Loaded {len(business_products_df)} products from {BUSINESS_PRODUCTS_PATH}")
        combined = pd.concat([original_metadata, business_products_df], ignore_index=True)
        print(f"Combined total: {len(combined)} products")
    else:
        print(f"{BUSINESS_PRODUCTS_PATH} not found. Using only original metadata.")
    
    # Set index and ensure it's integer type
    metadata = combined.set_index('id', drop=False)
    metadata.index = metadata.index.astype(int)
    print("--- Metadata Loading Complete ---")
    print(f"Metadata index type: {metadata.index.dtype}")
    print(f"Sample IDs: {list(metadata.index[:5])}")

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
    """Finds a product by its ID, with robust debugging."""
    global metadata
    
    # Ensure product_id is an integer
    try:
        product_id = int(product_id)
    except (ValueError, TypeError):
        logging.error(f"Invalid product_id format received: {product_id}")
        return None

    logging.info(f"--- Searching for product_id: {product_id} (type: {type(product_id)}) ---")
    
    # Check if metadata is loaded
    if metadata is None or metadata.empty:
        logging.error("Metadata DataFrame is not loaded or is empty!")
        return None

    logging.info(f"Metadata index type: {metadata.index.dtype}")
    logging.info(f"Is {product_id} in metadata.index? {product_id in metadata.index}")
    
    # This is the key check - let's see the actual values
    if product_id in metadata.index:
        logging.info(f"SUCCESS: Found product {product_id} in metadata.")
        return metadata.loc[product_id]
    else:
        # If not found, let's get some more info
        logging.warning(f"FAILURE: Product {product_id} NOT found in metadata index.")
        logging.info(f"First 10 IDs in metadata index: {list(metadata.index[:10])}")
        logging.info(f"Last 10 IDs in metadata index: {list(metadata.index[-10:])}")
        # Check if the ID exists in the 'id' column itself, just in case the index is messed up
        if product_id in metadata['id'].values:
            logging.warning(f"Product {product_id} found in 'id' column but not in the index! Index may be corrupted.")
        
        # Fallback to file (unlikely to be the issue, but good to check)
        logging.info(f"Checking fallback file: {BUSINESS_PRODUCTS_PATH}")
        try:
            business_df = pd.read_csv(BUSINESS_PRODUCTS_PATH, dtype={'id': int})
            product_rows = business_df[business_df['id'] == product_id]
            if not product_rows.empty:
                logging.info(f"Found product {product_id} in fallback file.")
                return product_rows.iloc[0]
        except FileNotFoundError:
            logging.warning(f"Fallback file not found: {BUSINESS_PRODUCTS_PATH}")
        except Exception as e:
            logging.error(f"Error reading fallback file: {e}")
            
        logging.error(f"Product {product_id} not found anywhere.")
        return None