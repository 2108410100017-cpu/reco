from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from config import IMAGE_DIR
from database import initialize_data

# -------------------------------
# INITIALIZE DATA FIRST (CRITICAL FIX)
# -------------------------------
initialize_data()

# Now import routers AFTER data is initialized
from routers import cart, products, admin, debug, recommendations, reviews_clean


# -------------------------------
# APP INIT
# -------------------------------
app = FastAPI(title="Image Recommendation API")


# -------------------------------
# CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://reco-2-diph.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# USER IDENTITY MIDDLEWARE
# -------------------------------
@app.middleware("http")
async def attach_user_identity(request: Request, call_next):
    """
    Centralized user identity handling.

    Priority:
    1. Frontend header: X-User-ID
    2. Fallback: 'guest'
    """

    user_id = request.headers.get("X-User-ID")

    if user_id:
        request.state.user_id = user_id.strip().lower()
    else:
        request.state.user_id = "guest"

    response = await call_next(request)
    return response


# -------------------------------
# STATIC IMAGES
# -------------------------------
if os.path.exists(IMAGE_DIR):
    app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")


# -------------------------------
# ROUTERS
# -------------------------------

app.include_router(products.router, tags=["products"])

app.include_router(
    recommendations.router,
    prefix="/products",
    tags=["recommendations"]
)

app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(admin.router, tags=["admin"])
app.include_router(debug.router, prefix="/debug", tags=["debug"])
app.include_router(reviews_clean.router, tags=["reviews-clean"])