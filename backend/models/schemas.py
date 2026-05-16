from pydantic import BaseModel
from typing import Optional, List, Any

class LoginRequest(BaseModel):
    email: str
    password: str

class CartItemRequest(BaseModel):
    product_id: Optional[int] = None
    qty: Optional[int] = 1
    quantity: Optional[int] = None

class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None

class OrderRequest(BaseModel):
    cart: List[Any] = []
    total: Optional[float] = 0

class PaymentRequest(BaseModel):
    method: str
    total: float