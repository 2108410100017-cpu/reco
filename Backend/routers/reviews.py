# backend/routers/reviews.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from database import add_review, get_reviews_by_product_id

router = APIRouter(prefix="/reviews", tags=["reviews"])

class ReviewIn(BaseModel):
    product_id: int
    rating: int
    comment: str

@router.post("/")
def create_review(review: ReviewIn):
    """Create a new review for a product."""
    # In a real app, the user_id would come from authentication.
    # For this demo, we generate a simple one.
    user_id = f"user-{uuid.uuid4().hex[:6]}"
    
    if not (1 <= review.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")
        
    new_review = add_review(review.product_id, user_id, review.rating, review.comment)
    return new_review

@router.get("/product/{product_id}")
def read_reviews(product_id: int):
    """Get all reviews for a specific product."""
    reviews = get_reviews_by_product_id(product_id)
    if not reviews:
        return {"message": "No reviews found for this product.", "reviews": []}
    return {"reviews": reviews}