import streamlit as st
from utils.session import init_session, is_logged_in
from utils.api_client import get_cart, update_cart_item, delete_cart_item
from utils.formatter import format_price
from components.style import inject_style
from components.toast import show_success, show_error
from utils.mock_data import MOCK_CATEGORIES

inject_style()
init_session()

st.markdown("""
    <div style='padding: 2rem 0 1rem'>
        <span style='font-size:0.68rem;letter-spacing:0.35em;text-transform:uppercase;color:#C9A96E'>Shopping</span>
        <h1 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:2.5rem'>
            My <em style='color:#C9A96E'>Cart</em>
        </h1>
        <div style='width:40px;height:1px;background:#C9A96E;margin-top:0.8rem'></div>
    </div>
""", unsafe_allow_html=True)

cart = get_cart()

if not cart:
    st.markdown("""
        <div style='text-align:center;padding:4rem 0;color:#8A8476'>
            <div style='font-size:3rem;margin-bottom:1rem'>◇</div>
            <p style='letter-spacing:0.1em'>Your cart is empty</p>
        </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Katalog.py", label="Browse Collection →")
else:
    col_items, col_summary = st.columns([2, 1])

    with col_items:
        for item in cart:
            c1, c2, c3 = st.columns([1, 3, 1])

            with c1:
                st.markdown(f"""
                    <div style='aspect-ratio:3/4;background:linear-gradient(135deg,#F5F0E8,#EDE5D5);
                    display:flex;align-items:center;justify-content:center;
                    font-family:"Cormorant Garamond",serif;font-style:italic;
                    color:#E8D5B0;font-size:1.5rem'>
                        {item["image_initial"]}
                    </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                    <div style='font-size:0.62rem;letter-spacing:0.25em;
                    text-transform:uppercase;color:#C9A96E;margin-bottom:0.3rem'>
                        {MOCK_CATEGORIES[item["category_id"]]}
                    </div>
                    <div style='font-family:"Cormorant Garamond",serif;font-size:1.1rem;
                    margin-bottom:0.8rem'>
                        {item["product_name"]}
                    </div>
                """, unsafe_allow_html=True)

                print(type("Quantity"))
                print(repr(item["qty"]))
                print(type(int(item["qty"])))
                print(st.__version__)

                new_qty = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=10,
                    value=int(item["qty"]),
                    key=f"qty_{item['cart_id']}"
                )
                if new_qty != item["qty"]:
                    update_cart_item(item["cart_id"], new_qty)
                    show_success("Quantity updated")
                    st.rerun()

                if st.button("Remove", key=f"del_{item['cart_id']}"):
                    delete_cart_item(item["cart_id"])
                    show_success("Item removed")
                    st.rerun()

            with c3:
                current_qty = st.session_state.get(f"qty_{item['cart_id']}", item["qty"])
                st.markdown(f"""
                    <div style='font-size:1rem;font-weight:500;text-align:right;padding-top:0.5rem'>
                       {format_price(item["price"] * current_qty)}
                    </div>
                """, unsafe_allow_html=True)

            st.divider()

    with col_summary:
        subtotal = sum(
            float(i["price"]) * st.session_state.get(f"qty_{i['cart_id']}", i["qty"])
            for i in cart
        )
        shipping = 0 if subtotal >= 500000 else 45000
        total = subtotal + shipping

        st.markdown(f"""
            <div style='border:1px solid rgba(201,169,110,0.25);padding:1.5rem'>
                <div style='font-family:"Cormorant Garamond",serif;font-size:1.5rem;
                margin-bottom:1.5rem;padding-bottom:1rem;
                border-bottom:1px solid rgba(201,169,110,0.25)'>
                    Order Summary
                </div>
                <div style='display:flex;justify-content:space-between;
                font-size:0.82rem;color:#8A8476;margin-bottom:0.8rem'>
                    <span>Subtotal</span><span>{format_price(subtotal)}</span>
                </div>
                <div style='display:flex;justify-content:space-between;
                font-size:0.82rem;color:#8A8476;margin-bottom:0.8rem'>
                    <span>Shipping</span>
                    <span>{'Free' if shipping == 0 else format_price(shipping)}</span>
                </div>
                <div style='display:flex;justify-content:space-between;
                font-size:1rem;font-weight:500;padding-top:1rem;
                border-top:1px solid rgba(201,169,110,0.25)'>
                    <span>Total</span><span>{format_price(total)}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.session_state["checkout_total"] = total
        st.session_state["checkout_cart"] = cart

        if st.button("Proceed to Checkout →", use_container_width=True):
            st.switch_page("pages/4_Checkout.py")
    
if new_qty != st.session_state.get(f"qty_{item['cart_id']}", item["qty"]):
    update_cart_item(item["cart_id"], new_qty)
    st.rerun()