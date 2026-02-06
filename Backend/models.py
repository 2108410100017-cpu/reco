from pydantic import BaseModel
from typing import List, Optional


# -------------------------------
# REQUEST MODELS
# -------------------------------
class RecommendRequest(BaseModel):
    query: str
    top_k: int = 10

    # NEW: Optional user identity
    user_id: Optional[str] = None


class BusinessProduct(BaseModel):
    business_id: Optional[str] = None
    name: str
    description: str = ""
    price: float

    # NEW: logged user fallback
    user_id: Optional[str] = None


# -------------------------------
# CART MODELS
# -------------------------------
class CartItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    image_url: str

    # NEW: optional ownership tracking
    user_id: Optional[str] = None


class Cart(BaseModel):
    items: List[CartItem]
    total_price: float

    # NEW: identifies cart owner
    user_id: Optional[str] = None
