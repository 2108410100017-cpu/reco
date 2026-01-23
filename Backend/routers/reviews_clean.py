# backend/routers/reviews_clean.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
import random
import uuid
from datetime import datetime, timedelta
from config import REVIEWS_PATH
print(f"\n>>> DEBUG: reviews_clean.py imported REVIEWS_PATH as: {REVIEWS_PATH}")

# --- Configuration ---
# --- FINAL FIX ---
# This finds the 'Training' directory by going up one level from 'backend'
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# TRAINING_DIR = os.path.join(BASE_DIR, "Training")
# REVIEWS_PATH = os.path.join(TRAINING_DIR, "reviews.csv")

print(f">>> FINAL DEBUG: Reading reviews from: {REVIEWS_PATH}")


# --- Pydantic Models ---
class ReviewIn(BaseModel):
    product_id: int
    rating: int
    comment: str

# --- Router ---
router = APIRouter(prefix="/reviews-clean", tags=["reviews-clean"])

# --- Helper Functions ---
# In backend/routers/reviews_clean.py, replace the existing load_reviews function

def load_reviews():
    """Loads reviews from the CSV file."""
    print(f"\n>>> FINAL DEBUG: Reading from the correct path: {REVIEWS_PATH}")
    
    if not os.path.exists(REVIEWS_PATH):
        print(f">>> WARNING: Reviews file not found at {REVIEWS_PATH}. Creating a new one.")
        os.makedirs(os.path.dirname(REVIEWS_PATH), exist_ok=True)
        pd.DataFrame(columns=['id', 'product_id', 'user_id', 'rating', 'comment', 'date']).to_csv(REVIEWS_PATH, index=False)
        return pd.DataFrame(columns=['id', 'product_id', 'user_id', 'rating', 'comment', 'date'])
    
    df = pd.read_csv(REVIEWS_PATH)
    print(f">>> SUCCESS: Read {len(df)} reviews from the file.")
    return df

def save_reviews(df):
    """Saves the reviews DataFrame to the CSV file."""
    df.to_csv(REVIEWS_PATH, index=False)

# --- API Endpoints ---
@router.get("/product/{product_id:int}")
def read_reviews(product_id: int):
    """Get all reviews for a specific product."""
    try:
        reviews_df = load_reviews()
        product_reviews = reviews_df[reviews_df['product_id'] == product_id]
        
        if product_reviews.empty:
            return {"message": "No reviews found for this product.", "reviews": []}
            
        return {"reviews": product_reviews.to_dict(orient="records")}
    except Exception as e:
        print(f">> ERROR in read_reviews: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/product/{product_id:int}")
def create_review(product_id: int, review: ReviewIn):
    """Create a new review."""
    try:
        reviews_df = load_reviews()
        
        if not (1 <= review.rating <= 5):
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")
            
        new_id = reviews_df['id'].max() + 1 if not reviews_df.empty else 1
        new_review = {
            'id': new_id,
            'product_id': product_id,
            'user_id': f"user-{uuid.uuid4().hex[:6]}",
            'rating': review.rating,
            'comment': review.comment,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        reviews_df = pd.concat([reviews_df, pd.DataFrame([new_review])], ignore_index=True)
        save_reviews(reviews_df)
        
        return new_review
    except Exception as e:
        print(f">> ERROR in create_review: {e}")
        raise HTTPException(status_code=500, detail=str(e))