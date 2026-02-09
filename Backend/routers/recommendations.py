from fastapi import APIRouter, HTTPException
import pandas as pd

router = APIRouter(tags=["recommendations"])


# -------------------------------
# RANDOM PRODUCTS
# -------------------------------
@router.get("/random")
def get_random_products(n: int = 12):
    """
    Fetch random products safely from metadata.
    """

    from database import metadata

    if len(metadata) == 0:
        return []

    metadata_for_sample = metadata.reset_index(drop=True).copy()
    random_products_df = metadata_for_sample.sample(
        n=min(n, len(metadata_for_sample))
    )

    def get_clean_image_url(row):
        try:
            if 'business_id' in row and pd.notna(row['business_id']):
                path = row['image_path']
                return (
                    f"/{path}"
                    if path.startswith('images/')
                    else f"/images/{path}"
                )

            return f"/images/{int(row['id'])}.jpg"

        except Exception:
            return "/images/placeholder.jpg"

    random_products_df['image_url'] = random_products_df.apply(
        get_clean_image_url,
        axis=1
    )

    return random_products_df.fillna('').to_dict(orient="records")


# -------------------------------
# SIMILAR PRODUCTS
# -------------------------------
@router.get("/similar/{product_id}")
def find_similar_products(product_id: int, top_k: int = 10):

    from database import metadata, image_embs, id_list

    if product_id not in metadata.index:
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found"
        )

    try:
        target_index = id_list.index(product_id)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Embedding not found"
        )

    target_embedding = image_embs[target_index]

    similarity_scores = (
        target_embedding @ image_embs.T
    ).squeeze(0)

    top_scores, top_indices = similarity_scores.topk(top_k)

    results = []

    for score, idx in zip(top_scores, top_indices):
        similar_pid = id_list[idx]

        if similar_pid == product_id:
            continue

        row = metadata.loc[similar_pid]

        price = float(row.get("price", 0.0))
        if pd.isna(price):
            price = 0.0

        image_url = ""
        if 'business_id' in row and pd.notna(row['business_id']):
            path = row['image_path']
            image_url = (
                f"/{path}"
                if path.startswith('images/')
                else f"/images/{path}"
            )
        else:
            image_url = f"/images/{similar_pid}.jpg"

        results.append({
            "id": int(similar_pid),
            "name": row.get("name", ""),
            "price": price,
            "score": float(score),
            "image_url": image_url,
            "added_date": row.get("added_date", "2026-01-01")
        })

    return results
