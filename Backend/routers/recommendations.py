# backend/routers/recommendations.py
from fastapi import APIRouter
from database import metadata
import pandas as pd

router = APIRouter(tags=["recommendations"])

@router.get("/random")
def get_random_products(n: int = 12):
    """
    Fetches a specified number of random products from the combined dataset.
    """
    print("--- /random endpoint called ---")
    
    # Import metadata inside the function
    from database import metadata
    
    print(f"Length of in-memory metadata DataFrame: {len(metadata)}")
    if len(metadata) == 0:
        print("!!! METADATA IS EMPTY. This is the problem. !!!")
        return []
    
    # Reset the index before sampling
    metadata_for_sample = metadata.reset_index(drop=True).copy()
    
    # Now, sample from the temporary DataFrame
    random_products_df = metadata_for_sample.sample(n=min(n, len(metadata_for_sample)))
    
    print(f"Length of sampled DataFrame: {len(random_products_df)}")

    def get_clean_image_url(row):
        try:
            if 'business_id' in row and pd.notna(row['business_id']):
                path = row['image_path']
                return f"/{path}" if path.startswith('images/') else f"/images/{path}"
            return f"/images/{int(row['id'])}.jpg"
        except Exception as e:
            print(f"Error creating image URL for row {row.get('id', 'unknown')}: {e}")
            return "/images/placeholder.jpg"

    random_products_df['image_url'] = random_products_df.apply(get_clean_image_url, axis=1)
    
    # Convert to a list of dictionaries
    result = random_products_df.fillna('').to_dict(orient="records")
    
    print(f"Length of final result list: {len(result)}")
    print("--- /random endpoint finished ---")
    
    return result