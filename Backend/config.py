import os

# -------------------------------
# PATH CONFIGURATION (UPDATED)
# -------------------------------

# Backend directory (where main.py exists)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Training folder is now INSIDE Backend
TRAIN_DIR = os.path.join(BASE_DIR, "Training")

# Core data files
EMB_PATH = os.path.join(TRAIN_DIR, "embeddings.pt")
META_PATH = os.path.join(TRAIN_DIR, "metadata.csv")
STYLES_PATH = os.path.join(TRAIN_DIR, "styles.csv")
IMAGE_DIR = os.path.join(TRAIN_DIR, "images")

# Training scripts
RETRAIN_SCRIPT_PATH = os.path.join(TRAIN_DIR, "retrain.py")
ADD_PRICES_SCRIPT_PATH = os.path.join(TRAIN_DIR, "add_prices.py")

# Business + metadata files
BUSINESS_PRODUCTS_PATH = os.path.join(TRAIN_DIR, "business_products.csv")
COMBINED_METADATA_PATH = os.path.join(TRAIN_DIR, "combined_metadata.csv")
REVIEWS_PATH = os.path.join(TRAIN_DIR, "reviews.csv")


# -------------------------------
# CART STORAGE (IDENTITY FIXED)
# -------------------------------

"""
Carts are stored per user:

carts[user_id] = {
    "items": [...],
    "total_price": float
}

User ID comes from frontend header:

X-User-ID

Fallback = 'guest'
"""

carts = {}


# -------------------------------
# BACKWARD COMPATIBILITY
# -------------------------------

DEFAULT_CART_ID = "guest"