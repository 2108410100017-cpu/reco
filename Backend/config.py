# backend/config.py
import os

# --- Paths ---
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

# --- Global State ---
carts = {}
DEFAULT_CART_ID = "default_cart"