from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import pandas as pd

from config import carts
from models import Cart
from database import get_product_by_id

router = APIRouter(tags=["cart"])


# ----------------------------------
# USER ID RESOLUTION (ROBUST)
# ----------------------------------
def get_user_id(request: Request):
    """
    User identity priority:

    1️⃣ Frontend header: X-User-ID
    2️⃣ Fallback → guest user

    Ensures:
    - No shared cart accidentally
    - No empty user_id
    """

    user_id = request.headers.get("X-User-ID")

    if not user_id or user_id.strip() == "":
        user_id = "guest"

    return user_id.strip()


# ----------------------------------
# DEBUG LOGGER (IMPORTANT)
# ----------------------------------
def log_cart_debug(user_id):
    print("\n===== CART DEBUG =====")
    print("User ID:", user_id)
    print("Active carts:", list(carts.keys()))
    print("======================\n")


# ----------------------------------
# ADD TO CART
# ----------------------------------
@router.post("/add", response_model=dict)
def add_to_cart(request: Request, product_id: int, quantity: int = 1):

    user_id = get_user_id(request)
    log_cart_debug(user_id)

    if user_id not in carts:
        carts[user_id] = {"items": [], "total_price": 0.0}

    cart = carts[user_id]

    product = get_product_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found."
        )

    # Image URL handling
    if 'business_id' in product and pd.notna(product['business_id']):
        path = product['image_path']
        image_url = f"/{path}" if path.startswith('images/') else f"/images/{path}"
    else:
        image_url = f"/images/{product_id}.jpg"

    # Add / update quantity
    for item in cart["items"]:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            break
    else:
        cart["items"].append({
            "product_id": int(product_id),
            "name": product["name"],
            "price": float(product["price"]),
            "quantity": quantity,
            "image_url": image_url
        })

    cart["total_price"] = sum(
        item["price"] * item["quantity"]
        for item in cart["items"]
    )

    return {
        "status": "success",
        "message": f"Added {product['name']} to cart."
    }


# ----------------------------------
# GET CART
# ----------------------------------
@router.get("/", response_model=Cart)
def get_cart(request: Request):

    user_id = get_user_id(request)
    log_cart_debug(user_id)

    if user_id not in carts:
        return {"items": [], "total_price": 0.0}

    return carts[user_id]


# ----------------------------------
# REMOVE ITEM
# ----------------------------------
@router.delete("/item/{product_id}", response_model=dict)
def remove_from_cart(request: Request, product_id: int):

    user_id = get_user_id(request)
    log_cart_debug(user_id)

    if user_id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart = carts[user_id]

    initial_length = len(cart["items"])
    cart["items"] = [
        item for item in cart["items"]
        if item["product_id"] != product_id
    ]

    if len(cart["items"]) == initial_length:
        raise HTTPException(status_code=404, detail="Item not found")

    cart["total_price"] = sum(
        item["price"] * item["quantity"]
        for item in cart["items"]
    )

    return {
        "status": "success",
        "message": "Item removed from cart."
    }


# ----------------------------------
# CLEAR CART
# ----------------------------------
@router.post("/clear", response_model=dict)
def clear_cart(request: Request):

    user_id = get_user_id(request)
    log_cart_debug(user_id)

    carts[user_id] = {"items": [], "total_price": 0.0}

    return {
        "status": "success",
        "message": "Cart cleared."
    }
