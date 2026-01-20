# backend/models.py
from pydantic import BaseModel
from typing import List, Optional

# Request Models
class RecommendRequest(BaseModel):
    query: str
    top_k: int = 10

class BusinessProduct(BaseModel):
    business_id: str
    name: str
    description: str = ""
    price: float

# Response Models
class CartItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    image_url: str

class Cart(BaseModel):
    items: List[CartItem]
    total_price: float