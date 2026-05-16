import streamlit as st
from utils.session import init_session
from utils.api_client import get_shipping_options, submit_payment, create_order
from utils.formatter import format_price
from components.style import inject_style
from components.toast import show_success, show_error

inject_style()
init_session()

if "checkout_step" not in st.session_state:
    st.session_state.checkout_step = 1

cart = st.session_state.get("checkout_cart", [])
total = st.session_state.get("checkout_total", 0)

# step indicator
steps = ["Shipping Address", "Payment", "Confirmation"]
cols = st.columns(3)
for i, (col, label) in enumerate(zip(cols, steps)):
    active = i + 1 == st.session_state.checkout_step
    done = i + 1 < st.session_state.checkout_step
    color = "#C9A96E" if active or done else "#8A8476"
    col.markdown(f"""
        <div style='text-align:center'>
            <div style='width:32px;height:32px;border-radius:50%;
            border:1px solid #C9A96E;display:inline-flex;align-items:center;
            justify-content:center;font-size:0.75rem;color:#C9A96E;
            background:{"#C9A96E" if done else "transparent"};
            color:{"white" if done else "#C9A96E"}'>
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
    st.markdown("<h3 style='font-family:\"Cormorant Garamond\",serif;font-weight:300'>Shipping <em style=\"color:#C9A96E\">Address</em></h3>", unsafe_allow_html=True)

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
    st.markdown("<h3 style='font-family:\"Cormorant Garamond\",serif;font-weight:300'>Payment <em style=\"color:#C9A96E\">Method</em></h3>", unsafe_allow_html=True)

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
                    result = submit_payment({"method": "credit_card", "total": final_total})
                    create_order({"cart": cart, "total": final_total})
                    st.session_state.order_id = "LM-20260516"
                    st.session_state.checkout_step = 3
                    st.rerun()
        else:
            final_total = total + ship_cost
            if st.button(f"place order · {format_price(final_total)}", use_container_width=True):
                result = submit_payment({"method": payment_method, "total": final_total})
                create_order({"cart": cart, "total": final_total})
                st.session_state.order_id = "LM-20260516"
                st.session_state.checkout_step = 3
                st.rerun()

    with col_order:
        st.markdown("<div style='font-family:\"Cormorant Garamond\",serif;font-size:1.2rem;margin-bottom:1rem'>Your Order</div>", unsafe_allow_html=True)
        for item in cart:
            st.markdown(f"""
                <div style='display:flex;justify-content:space-between;
                font-size:0.82rem;padding:0.5rem 0;
                border-bottom:1px solid rgba(201,169,110,0.25)'>
                    <span>{item['product_name']} ×{item['qty']}</span>
                    <span>{format_price(item['price'] * item['qty'])}</span>
                </div>
            """, unsafe_allow_html=True)

# step 3: konfirmasi
elif st.session_state.checkout_step == 3:
    order_id = st.session_state.get("order_id", "LM-20260516")
    st.markdown(f"""
        <div style='text-align:center;padding:4rem 0'>
            <div style='width:80px;height:80px;border-radius:50%;background:#E8F5E9;
            display:inline-flex;align-items:center;justify-content:center;
            font-size:2rem;color:#27AE60;margin-bottom:1.5rem'>✓</div>
            <span style='display:block;font-size:0.68rem;letter-spacing:0.35em;
            text-transform:uppercase;color:#C9A96E;margin-bottom:0.5rem'>order confirmed</span>
            <h2 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:2.5rem'>
                Thank <em style='color:#C9A96E'>You!</em>
            </h2>
            <p style='color:#8A8476;margin-top:0.8rem;font-size:0.85rem'>
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