import requests
import streamlit as st
from datetime import date   


BASE_URL = "http://localhost:8000"

USE_MOCK = True 

if USE_MOCK:
    from utils.mock_data import MOCK_CART, MOCK_ORDERS, MOCK_SHIPPING_OPTIONS, MOCK_USER

def get_headers():
    token = st.session_state.get("token", None)
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

# cart
def get_cart():
    if USE_MOCK:
        return MOCK_CART
    res = requests.get(f"{BASE_URL}/cart", headers=get_headers())
    return res.json() if res.ok else []

def add_to_cart(product_id, quantity=1):
    payload = {"product_id": product_id, "quantity": quantity}
    if USE_MOCK:
        MOCK_CART.append(payload)
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

# order
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

# shipping & payment
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

# profile
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