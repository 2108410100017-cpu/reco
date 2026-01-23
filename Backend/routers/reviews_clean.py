# backend/routers/reviews_clean.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
import uuid
from datetime import datetime
from config import REVIEWS_PATH

print(f"\n>>> DEBUG: reviews_clean.py imported REVIEWS_PATH as: {REVIEWS_PATH}")

# --- Pydantic Model ---
class ReviewIn(BaseModel):
    rating: int
    comment: str

# --- Router ---
router = APIRouter(prefix="/reviews-clean", tags=["reviews-clean"])

# --- Helper Functions ---
def load_reviews():
    """Load reviews from CSV file, create if it doesn't exist."""
    if not os.path.exists(REVIEWS_PATH):
        print(f">>> WARNING: Reviews file not found at {REVIEWS_PATH}. Creating a new one.")
        os.makedirs(os.path.dirname(REVIEWS_PATH), exist_ok=True)
        pd.DataFrame(columns=['id', 'product_id', 'user_id', 'rating', 'comment', 'date']).to_csv(REVIEWS_PATH, index=False)
        return pd.DataFrame(columns=['id', 'product_id', 'user_id', 'rating', 'comment', 'date'])
    
    df = pd.read_csv(REVIEWS_PATH)
    print(f">>> SUCCESS: Read {len(df)} reviews from the file.")
    return df

def save_reviews(df):
    """Save the reviews DataFrame to CSV."""
    df.to_csv(REVIEWS_PATH, index=False)
    print(f">>> SUCCESS: Saved {len(df)} reviews to {REVIEWS_PATH}")

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
    """Create a new review for a product."""
    print(f"\n>>> DEBUG: create_review called for product_id: {product_id}")
    print(f">>> DEBUG: Received review object: {review}")

    try:
        reviews_df = load_reviews()
        
        # Validate rating
        if not (1 <= review.rating <= 5):
            print(">>> ERROR: Validation failed - Rating is out of range.")
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")
        
        # Generate new review ID as Python int
        new_id = int(reviews_df['id'].max()) + 1 if not reviews_df.empty else 1

        new_review = {
            'id': new_id,
            'product_id': int(product_id),
            'user_id': f"user-{uuid.uuid4().hex[:6]}",
            'rating': int(review.rating),
            'comment': review.comment,
            'date': datetime.now().strftime('%Y-%m-%d')
        }

        print(f">>> DEBUG: Created new review: {new_review}")
        
        # Append and save
        reviews_df = pd.concat([reviews_df, pd.DataFrame([new_review])], ignore_index=True)
        save_reviews(reviews_df)
        
        print(">>> SUCCESS: Review saved successfully.")
        return new_review

    except Exception as e:
        print(f">>> FATAL ERROR in create_review: {e}")
        raise HTTPException(status_code=422, detail=str(e))
