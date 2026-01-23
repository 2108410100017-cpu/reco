# backend/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd

from config import IMAGE_DIR, COMBINED_METADATA_PATH
from database import initialize_data
from routers import cart, products, admin, debug, recommendations, reviews_clean

app = FastAPI(title="Image Recommendation API")


# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- STATIC IMAGES ----
if os.path.exists(IMAGE_DIR):
    app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")


# ---- STARTUP LOADS METADATA & EMBEDDINGS ----
@app.on_event("startup")
def startup_event():
    print(">>> STARTUP: Loading metadata...")

    try:
        if os.path.exists(COMBINED_METADATA_PATH):
            df = pd.read_csv(COMBINED_METADATA_PATH)
            df['id'] = df['id'].astype(int)
            app.state.product_metadata = df
            print(f">>> Metadata loaded: {len(df)} products")
        else:
            print(">>> WARNING: Metadata file missing:", COMBINED_METADATA_PATH)
            app.state.product_metadata = None

    except Exception as e:
        print(">>> ERROR loading metadata:", e)
        app.state.product_metadata = None

    initialize_data()
    print(">>> Startup complete.")


# ---- ROUTERS ----
app.include_router(products.router, tags=["products"])
app.include_router(recommendations.router, prefix="/products", tags=["recommendations"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(admin.router, tags=["admin"])
app.include_router(debug.router, prefix="/debug", tags=["debug"])
app.include_router(reviews_clean.router, tags=["reviews-clean"])


@app.get("/")
def root():
    return {"status": "ok", "msg": "Recommendation API online"}
