import os

# -------------------------------
# PATH CONFIGURATION (UNCHANGED)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_DIR = os.path.join(BASE_DIR, "../Training")

EMB_PATH = os.path.join(TRAIN_DIR, "embeddings.pt")
META_PATH = os.path.join(TRAIN_DIR, "metadata.csv")
STYLES_PATH = os.path.join(TRAIN_DIR, "styles.csv")
IMAGE_DIR = os.path.join(TRAIN_DIR, "images")

RETRAIN_SCRIPT_PATH = os.path.join(TRAIN_DIR, "retrain.py")
ADD_PRICES_SCRIPT_PATH = os.path.join(TRAIN_DIR, "add_prices.py")

BUSINESS_PRODUCTS_PATH = os.path.join(TRAIN_DIR, "business_products.csv")
COMBINED_METADATA_PATH = os.path.join(TRAIN_DIR, "combined_metadata.csv")

TRAINING_DIR_ABS = os.path.abspath(TRAIN_DIR)
REVIEWS_PATH = os.path.join(TRAINING_DIR_ABS, "reviews.csv")


# -------------------------------
# CART STORAGE (IDENTITY FIXED)
# -------------------------------
"""
Carts are now stored per user:

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
# Deprecated default cart ID.
# Do NOT use in new code.
DEFAULT_CART_ID = "guest"
