# backend/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from config import IMAGE_DIR
from database import initialize_data
from routers import cart, products, admin, debug

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

# Include all routers from the other files
app.include_router(cart.router)
app.include_router(products.router)
app.include_router(admin.router)
app.include_router(debug.router, prefix="/debug", tags=["debug"])

# Initialize data on startup
@app.on_event("startup")
def on_startup():
    initialize_data()