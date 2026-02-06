from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
import random
import uuid
from datetime import datetime
from config import REVIEWS_PATH


# -------------------------------
# Synthetic User Pool
# -------------------------------

USER_POOL = [f"user-{i:03d}" for i in range(1, 201)]


# -------------------------------
# Pydantic Model
# -------------------------------

class ReviewIn(BaseModel):
    product_id: int
    rating: int
    comment: str
    user_id: str | None = None   # frontend login user


router = APIRouter(prefix="/reviews-clean", tags=["reviews-clean"])


# -------------------------------
# Helper Functions
# -------------------------------

def load_reviews():
    """Load or create reviews CSV."""
    if not os.path.exists(REVIEWS_PATH):
        os.makedirs(os.path.dirname(REVIEWS_PATH), exist_ok=True)

        df = pd.DataFrame(
            columns=["id", "product_id", "user_id", "rating", "comment", "date"]
        )
        df.to_csv(REVIEWS_PATH, index=False)
        return df

    return pd.read_csv(REVIEWS_PATH)


def save_reviews(df):
    df.to_csv(REVIEWS_PATH, index=False)


# -------------------------------
# Get Reviews
# -------------------------------

@router.get("/product/{product_id:int}")
def read_reviews(product_id: int):
    try:
        df = load_reviews()
        reviews = df[df["product_id"] == product_id]

        if reviews.empty:
            return {"reviews": []}

        return {"reviews": reviews.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# Create Review (User-aware)
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

        # ⭐ Priority: Logged-in frontend user
        if review.user_id:
            user_id = review.user_id
        else:
            # fallback synthetic user
            user_id = random.choice(USER_POOL)

        new_id = (
            df["id"].max() + 1 if not df.empty else 1
        )

        new_review = {
            "id": new_id,
            "product_id": product_id,
            "user_id": user_id,
            "rating": review.rating,
            "comment": review.comment,
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
    """
    Creates synthetic reviews across many users/products
    for recommender system training.
    """

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
            new_id = (
                df["id"].max() + 1 if not df.empty else 1
            )

            new_review = {
                "id": new_id,
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
