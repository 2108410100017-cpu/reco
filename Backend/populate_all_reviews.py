# backend/populate_all_reviews.py
import pandas as pd
import os
import random
import uuid
from datetime import datetime, timedelta

# --- Configuration ---
# --- FIX IS HERE ---
# This correctly calculates the project root directory (the 'reco' folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAINING_DIR = os.path.join(BASE_DIR, "Training")
REVIEWS_PATH = os.path.join(TRAINING_DIR, "reviews.csv")
METADATA_PATH = os.path.join(TRAINING_DIR, "combined_metadata.csv")

print(f">>> DEBUG: Project Root (BASE_DIR): {BASE_DIR}")
print(f">>> DEBUG: Training Directory (TRAINING_DIR): {TRAINING_DIR}")
print(f">>> DEBUG: Reviews Path (REVIEWS_PATH): {REVIEWS_PATH}")
print(f">>> DEBUG: Metadata Path (METADATA_PATH): {METADATA_PATH}")


# --- Sample Data for Reviews ---
SAMPLE_COMMENTS = [
    "Absolutely love this! The quality is amazing.",
    "Great product, exactly as described.",
    "Fast shipping and excellent packaging.",
    "A bit smaller than I expected, but still good.",
    "Perfect fit. I've received so many compliments!",
    "The material feels a bit cheap.",
    "Good value for the price.",
    "Stunning! Looks even better in person.",
    "An okay purchase. Nothing special.",
    "Highly recommend! Will buy again.",
    "Color was slightly different from the picture.",
    "Very comfortable and well-made.",
    "Arrived with a small defect, but customer service was great.",
    "Exceeded my expectations. Fantastic!",
    "It's fine. Does what it's supposed to do."
]

def generate_random_review(product_id):
    """Generates a single random review for a given product ID."""
    return {
        "product_id": product_id,
        "user_id": f"user-{uuid.uuid4().hex[:6]}",
        "rating": random.randint(1, 5),
        "comment": random.choice(SAMPLE_COMMENTS),
        "date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
    }

# --- Main Logic ---
def main():
    print("Starting to populate reviews for all products...")

    # 1. Load all product IDs from combined_metadata.csv
    if not os.path.exists(METADATA_PATH):
        print(f"ERROR: Metadata file not found at {METADATA_PATH}")
        return

    metadata_df = pd.read_csv(METADATA_PATH, dtype={'id': int})
    all_product_ids = metadata_df['id'].tolist()
    print(f"Found {len(all_product_ids)} products in metadata.")

    # 2. Load existing reviews to avoid duplicates
    if os.path.exists(REVIEWS_PATH):
        existing_reviews_df = pd.read_csv(REVIEWS_PATH)
        print(f"Found {len(existing_reviews_df)} existing reviews.")
    else:
        existing_reviews_df = pd.DataFrame(columns=['id', 'product_id', 'user_id', 'rating', 'comment', 'date'])
        print("No existing reviews file found. Creating a new one.")

    # 3. Generate new reviews
    new_reviews = []
    next_id = existing_reviews_df['id'].max() + 1 if not existing_reviews_df.empty else 1

    for product_id in all_product_ids:
        # Let's add 1 to 3 random reviews per product
        num_reviews_to_add = random.randint(1, 3)
        for _ in range(num_reviews_to_add):
            review = generate_random_review(product_id)
            review['id'] = next_id
            new_reviews.append(review)
            next_id += 1

    print(f"Generated {len(new_reviews)} new reviews.")

    # 4. Combine with existing reviews and save
    all_reviews_df = pd.concat([existing_reviews_df, pd.DataFrame(new_reviews)], ignore_index=True)
    all_reviews_df.to_csv(REVIEWS_PATH, index=False)

    print(f"Successfully saved a total of {len(all_reviews_df)} reviews to {REVIEWS_PATH}")
    print("All done! You can now check the frontend.")

if __name__ == "__main__":
    main()