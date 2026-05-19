import requests
import streamlit as st
from datetime import date
from typing import Optional

BASE_URL = "http://localhost:8000"

USE_MOCK = True

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
    """List produk dengan filter, sort, dan search. Saat USE_MOCK=False
    akan diteruskan sebagai query params ke endpoint Dhimas (`GET /products`)."""
    if USE_MOCK:
        results = list(MOCK_PRODUCTS)

        if search:
            q = search.lower().strip()
            results = [
                p for p in results
                if q in p["product_name"].lower() or q in p["brand"].lower()
            ]
        if category_id is not None:
            results = [p for p in results if p["category_id"] == category_id]
        if brand:
            results = [p for p in results if p["brand"] == brand]
        if color:
            results = [p for p in results if p["color"] == color]
        if size:
            results = [p for p in results if p["size"] == size]
        if material:
            results = [p for p in results if p["material"] == material]
        if style:
            results = [p for p in results if p["style"] == style]
        if season:
            results = [p for p in results if p["season"] == season]
        if min_price is not None:
            results = [p for p in results if p["price"] >= min_price]
        if max_price is not None:
            results = [p for p in results if p["price"] <= max_price]

        if sort_by == "price_asc":
            results.sort(key=lambda p: p["price"])
        elif sort_by == "price_desc":
            results.sort(key=lambda p: p["price"], reverse=True)
        elif sort_by == "name_asc":
            results.sort(key=lambda p: p["product_name"].lower())
        else:  # newest = product_id desc (proxy karena tidak ada created_at)
            results.sort(key=lambda p: p["product_id"], reverse=True)

        if limit:
            results = results[:limit]
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
    """Ambil 1 produk untuk halaman detail."""
    if USE_MOCK:
        for p in MOCK_PRODUCTS:
            if p["product_id"] == int(product_id):
                return p
        return None
    res = requests.get(f"{BASE_URL}/products/{product_id}", headers=get_headers())
    return res.json() if res.ok else None


def get_categories():
    """List kategori untuk filter dropdown."""
    if USE_MOCK:
        return [{"category_id": cid, "category_name": name}
                for cid, name in MOCK_CATEGORIES.items()]
    res = requests.get(f"{BASE_URL}/categories", headers=get_headers())
    return res.json() if res.ok else []


def get_product_filter_options():
    """Daftar value unik (brand, color, dst) untuk populate dropdown filter.
    Real backend mestinya punya endpoint `/products/filters` yang return ini."""
    if USE_MOCK:
        return get_filter_options()
    res = requests.get(f"{BASE_URL}/products/filters", headers=get_headers())
    return res.json() if res.ok else {}


# ============================================================
# CART  
# ============================================================
def get_cart():
    if USE_MOCK:
        return MOCK_CART
    res = requests.get(f"{BASE_URL}/cart", headers=get_headers())
    return res.json() if res.ok else []

def add_to_cart(product_id, quantity=1):
    payload = {"product_id": product_id, "quantity": quantity}
    if USE_MOCK:
        # cek apakah item udah ada — kalau iya, tambah qty
        for item in MOCK_CART:
            if item.get("product_id") == product_id:
                item["qty"] = item.get("qty", 0) + quantity
                return item
        # enrich dengan info produk biar cart display-nya bener
        prod = get_product_by_id(product_id)
        if prod:
            new_item = {
                "cart_id": (max((i.get("cart_id", 1000) for i in MOCK_CART), default=1000) + 1),
                "customer_id": MOCK_USER["customer_id"],
                "product_id": prod["product_id"],
                "qty": quantity,
                "product_name": prod["product_name"],
                "brand": prod["brand"],
                "price": prod["price"],
                "color": prod["color"],
                "size": prod["size"],
                "material": prod["material"],
                "style": prod["style"],
                "season": prod["season"],
                "image_initial": prod["product_name"][0],
                "category_id": prod["category_id"],
            }
            MOCK_CART.append(new_item)
            return new_item
        return payload
    res = requests.post(f"{BASE_URL}/cart", json=payload, headers=get_headers())
    return res.json() if res.ok else None

def update_cart_item(item_id, quantity):
    payload = {"quantity": quantity}
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
            "items": [
                {
                    "product_name": item["product_name"],
                    "brand": item["brand"],
                    "qty": item["qty"],
                    "price_at_purchase": item["price"],
                }
                for item in payload.get("cart", [])
            ],
            "total": payload.get("total", 0),
        }
        MOCK_ORDERS.append(new_order)
        return new_order
    res = requests.post(f"{BASE_URL}/orders", json=payload, headers=get_headers())
    return res.json() if res.ok else None

def get_order_history():
    if USE_MOCK:
        return MOCK_ORDERS
    res = requests.get(f"{BASE_URL}/orders/history", headers=get_headers())
    return res.json() if res.ok else []

# ============================================================
# SHIPPING & PAYMENT  
# ============================================================
def get_shipping_options():
    if USE_MOCK:
        return MOCK_SHIPPING_OPTIONS
    res = requests.get(f"{BASE_URL}/shipping", headers=get_headers())
    return res.json() if res.ok else []

def submit_payment(payload):
    if USE_MOCK:
        return {"status": "success"}
    res = requests.post(f"{BASE_URL}/payment", json=payload, headers=get_headers())
    return res.json() if res.ok else None

# ============================================================
# PROFILE  
# ============================================================
def get_profile():
    if USE_MOCK:
        return MOCK_USER
    res = requests.get(f"{BASE_URL}/customer/profile", headers=get_headers())
    return res.json() if res.ok else {}

def update_profile(payload):
    if USE_MOCK:
        MOCK_USER.update(payload)
        return MOCK_USER
    res = requests.put(f"{BASE_URL}/customer/profile", json=payload, headers=get_headers())
    return res.json() if res.ok else None