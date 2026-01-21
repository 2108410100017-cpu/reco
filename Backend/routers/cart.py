# backend/routers/cart.py
from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import JSONResponse
import pandas as pd
import os
from config import carts, DEFAULT_CART_ID, BUSINESS_PRODUCTS_PATH
from models import Cart
from database import get_product_by_id

router = APIRouter(tags=["cart"])

@router.post("/add", response_model=dict)
def add_to_cart(product_id: int, quantity: int = 1):
    """Add a product to the cart."""
    if DEFAULT_CART_ID not in carts:
        carts[DEFAULT_CART_ID] = {"items": [], "total_price": 0.0}

    cart = carts[DEFAULT_CART_ID]
    
    # FIX: The function returns a pandas Series. Check if it's None.
    product = get_product_by_id(product_id)
    
    # FIX: Use an explicit check for None
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")

    image_url = ""
    # product is now a pandas Series, so you can access columns with .column_name
    if 'business_id' in product and pd.notna(product['business_id']):
        path = product['image_path']
        image_url = f"/{path}" if path.startswith('images/') else f"/images/{path}"
    else:
        image_url = f"/images/{product_id}.jpg"

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

    cart["total_price"] = sum(item["price"] * item["quantity"] for item in cart["items"])
    return {"status": "success", "message": f"Added {product['name']} to cart."}

@router.get("/", response_model=Cart)
def get_cart():
    """Get the current cart contents."""
    if DEFAULT_CART_ID not in carts:
        return {"items": [], "total_price": 0.0}
    return carts[DEFAULT_CART_ID]

@router.delete("/item/{product_id}", response_model=dict)
def remove_from_cart(product_id: int):
    """Remove an item from the cart."""
    if DEFAULT_CART_ID not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart = carts[DEFAULT_CART_ID]
    initial_length = len(cart["items"])
    cart["items"] = [item for item in cart["items"] if item["product_id"] != product_id]
    
    if len(cart["items"]) == initial_length:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    cart["total_price"] = sum(item["price"] * item["quantity"] for item in cart["items"])
    return {"status": "success", "message": "Item removed from cart."}

@router.post("/clear", response_model=dict)
def clear_cart():
    """Clear all items from the cart."""
    carts[DEFAULT_CART_ID] = {"items": [], "total_price": 0.0}
    return {"status": "success", "message": "Cart cleared."}