import os
import pandas as pd
import torch
import logging

from config import (
    EMB_PATH,
    META_PATH,
    BUSINESS_PRODUCTS_PATH,
    IMAGE_DIR,
    RETRAIN_SCRIPT_PATH,
    ADD_PRICES_SCRIPT_PATH
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------
# GLOBAL STATE
# -------------------------------
metadata = None
business_products = None
emb = None
image_embs = None
text_embs = None
id_list = None


# -------------------------------
# METADATA LOADER
# -------------------------------
def load_combined_metadata():
    """Load original + business products safely."""

    global metadata

    logging.info("Loading combined metadata...")

    if not os.path.exists(META_PATH):
        raise RuntimeError("metadata.csv missing")

    # Load original metadata
    original_metadata = pd.read_csv(META_PATH, dtype={'id': int})

    combined = original_metadata

    if os.path.exists(BUSINESS_PRODUCTS_PATH):
        business_products_df = pd.read_csv(
            BUSINESS_PRODUCTS_PATH,
            dtype={'id': int}
        )

        # -------- IDENTITY FIX --------
        if 'business_id' in business_products_df.columns:
            business_products_df['business_id'] = (
                business_products_df['business_id']
                .astype(str)
                .str.strip()
            )

        combined = pd.concat(
            [original_metadata, business_products_df],
            ignore_index=True
        )

    metadata = combined.set_index('id', drop=False)
    metadata.index = metadata.index.astype(int)

    logging.info(f"Metadata loaded: {len(metadata)} products")


# -------------------------------
# INITIALIZATION
# -------------------------------
def initialize_data():
    """Load metadata + embeddings at startup."""

    global metadata, emb, image_embs, text_embs, id_list

    load_combined_metadata()

    # Ensure business products file exists
    if not os.path.exists(BUSINESS_PRODUCTS_PATH):
        pd.DataFrame(
            columns=[
                'id', 'business_id', 'name',
                'description', 'price',
                'image_path', 'added_date'
            ]
        ).to_csv(BUSINESS_PRODUCTS_PATH, index=False)

    if not os.path.exists(EMB_PATH):
        raise RuntimeError("embeddings.pt missing. Run retrain first.")

    emb = torch.load(EMB_PATH, map_location="cpu")

    image_embs = emb['image_embeddings']
    text_embs = emb['text_embeddings']

    image_embs = image_embs / image_embs.norm(dim=-1, keepdim=True)

    if 'valid_ids' in emb:
        id_list = emb['valid_ids']
    else:
        logging.warning(
            "'valid_ids' missing in embeddings.pt. "
            "Using metadata IDs."
        )
        id_list = metadata['id'].tolist()


# -------------------------------
# PRODUCT LOOKUP
# -------------------------------
def get_product_by_id(product_id: int):
    """Robust product lookup."""

    global metadata

    try:
        product_id = int(product_id)
    except (ValueError, TypeError):
        logging.error(f"Invalid product_id: {product_id}")
        return None

    if metadata is None or metadata.empty:
        logging.error("Metadata not initialized")
        return None

    if product_id in metadata.index:
        return metadata.loc[product_id]

    logging.warning(f"Product {product_id} not in metadata")

    # fallback business file
    try:
        business_df = pd.read_csv(
            BUSINESS_PRODUCTS_PATH,
            dtype={'id': int}
        )

        rows = business_df[business_df['id'] == product_id]
        if not rows.empty:
            return rows.iloc[0]

    except Exception as e:
        logging.error(f"Fallback lookup error: {e}")

    return None
