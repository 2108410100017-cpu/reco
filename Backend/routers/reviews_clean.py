from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
import random
from datetime import datetime
from config import REVIEWS_PATH


# -------------------------------
# Synthetic User Pool
# -------------------------------
USER_POOL = [f"user-{i:03d}" for i in range(1, 201)]


# -------------------------------
# Review Model
# -------------------------------
class ReviewIn(BaseModel):
    product_id: int
    rating: int
    comment: str
    user_id: str | None = None


router = APIRouter(prefix="/reviews-clean", tags=["reviews-clean"])


# -------------------------------
# Helpers
# -------------------------------
def normalize_user(user_id: str | None):
    if not user_id:
        return random.choice(USER_POOL)
    return str(user_id).strip().lower()


def load_reviews():
    """Load or initialize review storage."""
    if not os.path.exists(REVIEWS_PATH):
        os.makedirs(os.path.dirname(REVIEWS_PATH), exist_ok=True)

        df = pd.DataFrame(
            columns=["id", "product_id", "user_id", "rating", "comment", "date"]
        )
        df.to_csv(REVIEWS_PATH, index=False)
        return df

    df = pd.read_csv(REVIEWS_PATH)

    # Ensure consistent types
    if "user_id" in df.columns:
        df["user_id"] = df["user_id"].astype(str)

    return df


def save_reviews(df):
    df.to_csv(REVIEWS_PATH, index=False)


def next_review_id(df):
    if df.empty:
        return 1
    return int(pd.to_numeric(df["id"], errors="coerce").max()) + 1


# -------------------------------
# Get Reviews
# -------------------------------
@router.get("/product/{product_id:int}")
def read_reviews(product_id: int):
    try:
        df = load_reviews()
        reviews = df[df["product_id"] == product_id]

        return {"reviews": reviews.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# Create Review
# -------------------------------
@router.post("/product/{product_id:int}")
def create_review(product_id: int, review: ReviewIn):
    try:
        df = load_reviews()

        if not (1 <= review.rating <= 5):
            raise HTTPException(
                status_code=400,
                detail="Rating must be between 1 and 5."
            )

        user_id = normalize_user(review.user_id)

        new_review = {
            "id": next_review_id(df),
            "product_id": int(product_id),
            "user_id": user_id,
            "rating": int(review.rating),
            "comment": review.comment.strip(),
            "date": datetime.now().strftime("%Y-%m-%d"),
        }

        df = pd.concat([df, pd.DataFrame([new_review])], ignore_index=True)
        save_reviews(df)

        return new_review

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# Generate Dummy Reviews
# -------------------------------
@router.post("/generate-dummy-reviews")
def generate_dummy_reviews(num_reviews: int = 500):

    try:
        df = load_reviews()

        comments = [
            "Great product",
            "Nice quality",
            "Loved it",
            "Worth buying",
            "Could be better",
            "Amazing experience",
            "Not satisfied",
            "Very comfortable",
            "Premium feel",
            "Highly recommended"
        ]

        for _ in range(num_reviews):
            new_review = {
                "id": next_review_id(df),
                "product_id": random.randint(1, 10000),
                "user_id": random.choice(USER_POOL),
                "rating": random.randint(1, 5),
                "comment": random.choice(comments),
                "date": datetime.now().strftime("%Y-%m-%d"),
            }

            df = pd.concat([df, pd.DataFrame([new_review])], ignore_index=True)

        save_reviews(df)

        return {"message": f"{num_reviews} synthetic reviews generated"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
