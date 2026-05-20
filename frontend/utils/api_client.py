import requests
import streamlit as st
from datetime import date
from typing import Optional

BASE_URL = "http://localhost:8000"

USE_MOCK = False

if USE_MOCK:
    from utils.mock_data import (
        MOCK_CART, MOCK_ORDERS, MOCK_SHIPPING_OPTIONS, MOCK_USER,
        MOCK_PRODUCTS, MOCK_CATEGORIES, get_filter_options,
    )

def get_headers():
    token = st.session_state.get("token", None)
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

# ============================================================
# PRODUCTS  
# ============================================================
def get_products(
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    brand: Optional[str] = None,
    color: Optional[str] = None,
    size: Optional[str] = None,
    material: Optional[str] = None,
    style: Optional[str] = None,
    season: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "newest",   # newest | price_asc | price_desc | name_asc
    limit: Optional[int] = None,
):
    if USE_MOCK:
        results = list(MOCK_PRODUCTS)
        if search:
            q = search.lower().strip()
            results = [p for p in results if q in p["name"].lower() or q in p["brand"].lower()]
        if category_id is not None:
            results = [p for p in results if p["category_id"] == category_id]
        if sort_by == "price_asc": results.sort(key=lambda p: p["price"])
        elif sort_by == "price_desc": results.sort(key=lambda p: p["price"], reverse=True)
        if limit: results = results[:limit]
        return results

    params = {
        "search": search, "category_id": category_id, "brand": brand,
        "color": color, "size": size, "material": material, "style": style,
        "season": season, "min_price": min_price, "max_price": max_price,
        "sort_by": sort_by, "limit": limit,
    }
    params = {k: v for k, v in params.items() if v is not None}
    res = requests.get(f"{BASE_URL}/products", params=params, headers=get_headers())
    return res.json() if res.ok else []

def get_product_by_id(product_id: int):
    if USE_MOCK:
        for p in MOCK_PRODUCTS:
            if p["product_id"] == int(product_id): return p
        return None
    res = requests.get(f"{BASE_URL}/products/{product_id}", headers=get_headers())
    return res.json() if res.ok else None

def get_categories():
    if USE_MOCK:
        return [{"category_id": cid, "category_name": name} for cid, name in MOCK_CATEGORIES.items()]
    res = requests.get(f"{BASE_URL}/categories", headers=get_headers())
    return res.json() if res.ok else []

def create_product(data, files):
    res = requests.post(f"{BASE_URL}/products", data=data, files=files, headers=get_headers())
    return res.json() if res.ok else None

def update_product(product_id, data, files=None):
    res = requests.put(f"{BASE_URL}/products/{product_id}", data=data, files=files, headers=get_headers())
    return res.json() if res.ok else None

def delete_product(product_id):
    res = requests.delete(f"{BASE_URL}/products/{product_id}", headers=get_headers())
    return res.ok

# ============================================================
# CART  
# ============================================================
def get_cart():
    if USE_MOCK: return MOCK_CART
    res = requests.get(f"{BASE_URL}/cart", headers=get_headers())
    return res.json() if res.ok else []

def add_to_cart(product_id, quantity=1):
    payload = {"product_id": product_id, "qty": quantity}
    if USE_MOCK:
        for item in MOCK_CART:
            if item.get("product_id") == product_id:
                item["qty"] = item.get("qty", 0) + quantity
                return item
        prod = get_product_by_id(product_id)
        if prod:
            new_item = {
                "cart_id": (max((i.get("cart_id", 1000) for i in MOCK_CART), default=1000) + 1),
                "product_id": prod["product_id"], "qty": quantity, "name": prod["name"],
                "price": prod["price"], "image_initial": prod["name"][0],
            }
            MOCK_CART.append(new_item)
            return new_item
        return payload
    
    headers = get_headers()
    print(f"[add_to_cart] Sending request to {BASE_URL}/cart with payload: {payload}")
    print(f"[add_to_cart] Headers: {headers}")
    res = requests.post(f"{BASE_URL}/cart", json=payload, headers=headers)
    print(f"[add_to_cart] Response status: {res.status_code}")
    print(f"[add_to_cart] Response body: {res.text}")
    
    if res.ok:
        result = res.json()
        print(f"[add_to_cart] Success: {result}")
        return result
    else:
        error_data = res.json() if res.text else {"error": f"HTTP {res.status_code}"}
        print(f"[add_to_cart] Failed: {error_data}")
        return error_data

def update_cart_item(item_id, quantity):
    payload = {"qty": quantity}
    if USE_MOCK:
        for item in MOCK_CART:
            if item["cart_id"] == item_id:
                item["qty"] = quantity
                return item
        return None
    res = requests.put(f"{BASE_URL}/cart/{item_id}", json=payload, headers=get_headers())
    return res.json() if res.ok else None

def delete_cart_item(item_id):
    if USE_MOCK:
        global MOCK_CART
        MOCK_CART = [item for item in MOCK_CART if item["cart_id"] != item_id]
        return True
    res = requests.delete(f"{BASE_URL}/cart/{item_id}", headers=get_headers())
    return res.ok

# ============================================================
# ORDER 
# ============================================================
def create_order(payload):
    if USE_MOCK:
        new_order = {
            "order_id": f"LM-{str(len(MOCK_ORDERS) + 1).zfill(3)}",
            "date": date.today().strftime("%d %B %Y"),
            "status": "processing",
            "items": [], "total": payload.get("total", 0),
        }
        MOCK_ORDERS.append(new_order)
        return new_order
    res = requests.post(f"{BASE_URL}/orders", json=payload, headers=get_headers())
    return res.json() if res.ok else None

def get_order_history():
    if USE_MOCK: return MOCK_ORDERS
    res = requests.get(f"{BASE_URL}/orders/history", headers=get_headers())
    return res.json() if res.ok else []

def submit_payment(payload):
    """Submit payment with method and total amount"""
    if USE_MOCK:
        return {"status": "success", "message": "Payment processed"}
    res = requests.post(f"{BASE_URL}/payment", json=payload, headers=get_headers())
    return res.json() if res.ok else None

# ============================================================
# SHIPPING  
# ============================================================
def get_shipping_options():
    """Get available shipping options"""
    if USE_MOCK:
        return [
            {"name": "Standard", "estimate": "5-7 days", "price": 50000},
            {"name": "Express", "estimate": "2-3 days", "price": 100000},
            {"name": "Overnight", "estimate": "Next day", "price": 150000},
        ]
    res = requests.get(f"{BASE_URL}/shipping/options", headers=get_headers())
    if res.ok:
        return res.json()
    # Fallback dengan default options kalau API gagal
    return [
        {"name": "Standard", "estimate": "5-7 days", "price": 50000},
        {"name": "Express", "estimate": "2-3 days", "price": 100000},
        {"name": "Overnight", "estimate": "Next day", "price": 150000},
    ]

# ============================================================
# ADMIN  
# ============================================================
def get_admin_stats():
    res = requests.get(f"{BASE_URL}/admin/stats", headers=get_headers())
    return res.json() if res.ok else {}

def get_admin_orders():
    res = requests.get(f"{BASE_URL}/admin/orders", headers=get_headers())
    return res.json() if res.ok else []

def admin_update_order_status(order_id, status):
    data = {"status": status}
    res = requests.put(f"{BASE_URL}/admin/orders/{order_id}/status", data=data, headers=get_headers())
    return res.json() if res.ok else None

# ============================================================
# AUTH  
# ============================================================
def login(email, password):
    payload = {"email": email, "password": password}
    res = requests.post(f"{BASE_URL}/login", json=payload)
    return res.json() if res.ok else None

def register(email, password, first_name, last_name, phone_number):
    payload = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number
    }
    try:
        res = requests.post(f"{BASE_URL}/register", json=payload)
        return res.json()
    except Exception:
        return {"detail": "Tidak dapat terhubung ke server."}

def logout_api():
    res = requests.post(f"{BASE_URL}/logout", headers=get_headers())
    return res.ok

# ============================================================
# PROFILE  
# ============================================================
def get_profile():
    if USE_MOCK: return MOCK_USER
    res = requests.get(f"{BASE_URL}/customer/profile", headers=get_headers())
    return res.json() if res.ok else {}

def update_profile(payload):
    if USE_MOCK:
        MOCK_USER.update(payload)
        return MOCK_USER
    res = requests.put(f"{BASE_URL}/customer/profile", json=payload, headers=get_headers())
    return res.json() if res.ok else None
