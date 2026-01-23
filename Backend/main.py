# backend/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from routers import reviews_clean
from config import IMAGE_DIR
from database import initialize_data
from routers import cart, products, admin, debug, recommendations # NEW IMPORT

# Create the FastAPI app instance
app = FastAPI(title="Image Recommendation API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists(IMAGE_DIR):
    app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

# --- CORRECTED ROUTER INCLUSIONS ---
# The main products router has NO prefix, so /recommend and /latest work at the root level.
app.include_router(products.router, tags=["products"])

# The new recommendations router has the /products prefix.
app.include_router(recommendations.router, prefix="/products", tags=["recommendations"])

# Other routers
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(admin.router, tags=["admin"])
app.include_router(debug.router, prefix="/debug", tags=["debug"])
app.include_router(reviews_clean.router, tags=["reviews-clean"])

# Initialize data on startup
@app.on_event("startup")
def on_startup():
    initialize_data()