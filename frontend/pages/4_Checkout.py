import streamlit as st

# WAJIB: set_page_config harus menjadi perintah Streamlit pertama
st.set_page_config(page_title="Checkout - Lumière", page_icon="💳", layout="wide")

from utils.session import init_session
from utils.api_client import get_shipping_options, submit_payment, create_order
from utils.formatter import format_price
from components.style import inject_style
from components.navbar import render_navbar
from components.toast import show_success, show_error

init_session()
inject_style()
render_navbar()

if "checkout_step" not in st.session_state:
    st.session_state.checkout_step = 1

cart = st.session_state.get("checkout_cart", [])
stored_total = st.session_state.get("checkout_total", 0)
subtotal = sum(
    item.get("price", 0) * item.get("qty", item.get("quantity", 1))
    for item in cart
) if cart else stored_total
total = subtotal

def clear_checkout_cart_state():
    qty_keys = [key for key in st.session_state.keys() if key.startswith("qty_")]
    for key in qty_keys:
        del st.session_state[key]
    st.session_state.pop("checkout_cart", None)
    st.session_state.pop("checkout_total", None)

def get_item_qty(item):
    return int(item.get("qty", item.get("quantity", 1)) or 1)

def get_item_name(item):
    return item.get("product_name") or item.get("name") or "Product"

def get_payment_value(payment_method):
    if "bank transfer" in payment_method:
        return "tf_bank"
    if "e-wallet" in payment_method:
        return "gopay"
    return "tf_bank"

def build_order_payload(final_total, payment_method):
    address = st.session_state.get("shipping_address", {})
    return {
        "cart": cart,
        "total": final_total,
        "shipping_address": address.get("address", ""),
        "city": address.get("city", ""),
        "postal_code": address.get("postal", ""),
        "payment_method": payment_method,
    }

def show_order_error(order_response):
    message = "Failed to create order. Please try again."
    if isinstance(order_response, dict):
        message = order_response.get("detail") or order_response.get("message") or message
    show_error(message)

# step indicator
steps = ["Shipping Address", "Payment", "Confirmation"]
cols = st.columns(3)
for i, (col, label) in enumerate(zip(cols, steps)):
    active = i + 1 == st.session_state.checkout_step
    done = i + 1 < st.session_state.checkout_step
    color = "var(--gold)" if active or done else "var(--text-muted)"
    bg_color = "var(--gold)" if done else "transparent"
    text_color = "white" if done else "var(--gold)"
    col.markdown(f"""
        <div style='text-align:center'>
            <div style='width:32px;height:32px;border-radius:50%;
            border:1px solid var(--gold);display:inline-flex;align-items:center;
            justify-content:center;font-size:0.75rem;color:{text_color};
            background:{bg_color}'>
                {"✓" if done else i+1}
            </div>
            <div style='font-size:0.72rem;letter-spacing:0.1em;
            text-transform:uppercase;color:{color};margin-top:0.4rem'>
                {label}
            </div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# step 1: alamat
if st.session_state.checkout_step == 1:
    st.markdown("<h3 style='font-family:\"Cormorant Garamond\",serif;font-weight:300;color:var(--text);'>Shipping <em style=\"color:var(--gold)\">Address</em></h3>", unsafe_allow_html=True)

    with st.form("address_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("full name", placeholder="Aliya Lumière")
        phone = c2.text_input("phone", placeholder="+62 812-345-6789")
        address = st.text_input("street address", placeholder="Jl. Sudirman No. 10")
        c3, c4 = st.columns(2)
        city = c3.text_input("city", placeholder="Jakarta Selatan")
        postal = c4.text_input("postal code", placeholder="12345")

        if st.form_submit_button("continue to payment →", use_container_width=True):
            if name and address and city:
                st.session_state.shipping_address = {
                    "name": name, "phone": phone,
                    "address": address, "city": city, "postal": postal,
                }
                st.session_state.checkout_step = 2
                st.rerun()
            else:
                show_error("please fill in all required fields")

# step 2: payment
elif st.session_state.checkout_step == 2:
    st.markdown("<h3 style='font-family:\"Cormorant Garamond\",serif;font-weight:300;color:var(--text);'>Payment <em style=\"color:var(--gold)\">Method</em></h3>", unsafe_allow_html=True)

    col_form, col_order = st.columns([3, 2])

    with col_form:
        shipping_options = get_shipping_options()
        ship_labels = [f"{s['name']} — {s['estimate']} ({format_price(s['price'])})" for s in shipping_options]
        selected_ship = st.radio("shipping option", ship_labels, label_visibility="collapsed")
        ship_idx = ship_labels.index(selected_ship)
        ship_cost = shipping_options[ship_idx]["price"]

        payment_method = st.radio(
            "payment method",
            ["💳 credit card", "🏦 bank transfer", "📱 e-wallet"],
            label_visibility="collapsed",
        )

        if "credit card" in payment_method:
            with st.form("card_form"):
                card_name = st.text_input("name on card", placeholder="ALIYA LUMIÈRE")
                card_number = st.text_input("card number", placeholder="4242 4242 4242 4242", max_chars=19)
                c1, c2 = st.columns(2)
                expiry = c1.text_input("expiry", placeholder="MM / YY")
                cvv = c2.text_input("cvv", placeholder="•••", max_chars=3, type="password")

                final_total = total + ship_cost
                if st.form_submit_button(f"place order · {format_price(final_total)}", use_container_width=True):
                    payment_value = get_payment_value(payment_method)
                    result = submit_payment({"method": payment_value, "total": final_total})
                    order_response = create_order(build_order_payload(final_total, payment_value))
                    if order_response and "order_id" in order_response:
                        st.session_state.order_id = order_response["order_id"]
                        clear_checkout_cart_state()
                        st.session_state.checkout_step = 3
                        st.rerun()
                    else:
                        show_order_error(order_response)
        else:
            final_total = total + ship_cost
            if st.button(f"place order · {format_price(final_total)}", use_container_width=True):
                payment_value = get_payment_value(payment_method)
                result = submit_payment({"method": payment_value, "total": final_total})
                order_response = create_order(build_order_payload(final_total, payment_value))
                if order_response and "order_id" in order_response:
                    st.session_state.order_id = order_response["order_id"]
                    clear_checkout_cart_state()
                    st.session_state.checkout_step = 3
                    st.rerun()
                else:
                    show_order_error(order_response)

    with col_order:
        st.markdown("<div style='font-family:\"Cormorant Garamond\",serif;font-size:1.2rem;margin-bottom:1rem;color:var(--text);'>Your Order</div>", unsafe_allow_html=True)
        for item in cart:
            item_qty = get_item_qty(item)
            item_price = item.get("price", 0)
            item["product_name"] = get_item_name(item)
            item["qty"] = item_qty
            st.markdown(f"""
                <div style='display:flex;justify-content:space-between;
                font-size:0.82rem;padding:0.5rem 0;
                border-bottom:1px solid var(--border);color:var(--text)'>
                    <span>{item['product_name']} ×{item['qty']}</span>
                    <span>{format_price(item_price * item_qty)}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
            <div style='display:flex;justify-content:space-between;
            font-size:0.82rem;padding:0.7rem 0 0.4rem;color:var(--text-muted)'>
                <span>Subtotal</span>
                <span>{format_price(total)}</span>
            </div>
            <div style='display:flex;justify-content:space-between;
            font-size:0.82rem;padding:0.2rem 0 0.7rem;color:var(--text-muted)'>
                <span>Shipping</span>
                <span>{'Free' if ship_cost == 0 else format_price(ship_cost)}</span>
            </div>
            <div style='display:flex;justify-content:space-between;
            font-size:1rem;font-weight:500;padding-top:0.8rem;
            border-top:1px solid var(--border);color:var(--text)'>
                <span>Total</span>
                <span>{format_price(total + ship_cost)}</span>
            </div>
        """, unsafe_allow_html=True)

# step 3: konfirmasi
elif st.session_state.checkout_step == 3:
    order_id = st.session_state.get("order_id", "LM-20260516")
    st.markdown(f"""
        <div style='text-align:center;padding:4rem 0'>
            <div style='width:80px;height:80px;border-radius:50%;background:rgba(39, 174, 96, 0.1);
            display:inline-flex;align-items:center;justify-content:center;
            font-size:2rem;color:var(--success);margin-bottom:1.5rem'>✓</div>
            <span style='display:block;font-size:0.68rem;letter-spacing:0.35em;
            text-transform:uppercase;color:var(--gold);margin-bottom:0.5rem'>order confirmed</span>
            <h2 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:2.5rem;color:var(--text);'>
                Thank <em style='color:var(--gold)'>You!</em>
            </h2>
            <p style='color:var(--text-muted);margin-top:0.8rem;font-size:0.85rem'>
                order <strong>{order_id}</strong> has been confirmed
            </p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("track order →", use_container_width=True):
            st.session_state.checkout_step = 1
            st.switch_page("pages/5_Riwayat.py")
    with c2:
        if st.button("continue shopping", use_container_width=True):
            st.session_state.checkout_step = 1
            st.switch_page("pages/1_Katalog.py")
