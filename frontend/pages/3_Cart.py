import streamlit as st

# WAJIB: set_page_config harus menjadi perintah Streamlit pertama sebelum import lokal/komponen lain
st.set_page_config(page_title="My Cart - Lumière", page_icon="🛒", layout="wide")

from utils.session import init_session, is_logged_in
from utils.api_client import get_cart, update_cart_item, delete_cart_item
from utils.formatter import format_price
from components.style import inject_style
from components.navbar import render_navbar
from components.toast import show_success, show_error
from utils.mock_data import MOCK_CATEGORIES

# Inisialisasi tampilan dan session
init_session()
inject_style()
render_navbar()

st.markdown("""
    <div style='padding: 2rem 0 1rem'>
        <span style='font-size:0.68rem;letter-spacing:0.35em;text-transform:uppercase;color:var(--gold)'>Shopping</span>
        <h1 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:2.5rem;color:var(--text)'>
            My <em style='color:var(--gold)'>Cart</em>
        </h1>
        <div style='width:40px;height:1px;background:var(--gold);margin-top:0.8rem'></div>
    </div>
""", unsafe_allow_html=True)

# Pengecekan status login pelanggan
if not is_logged_in():
    st.warning("Silakan login terlebih dahulu untuk melihat keranjang belanja Anda.")
    st.stop()

cart = get_cart()

if not cart:
    st.markdown("""
        <div style='text-align:center;padding:4rem 0;color:var(--text-muted)'>
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
            
            # Amankan variabel menggunakan .get() untuk menghindari KeyError
            cart_id = item.get("cart_id")
            product_name = item.get("product_name", "Product")
            qty = item.get("qty", 1)
            price = item.get("price", 0)
            category_id = item.get("category_id")
            image_url = item.get("image_url")

            with c1:
                if image_url:
                    st.markdown(f"""
                        <img src="{image_url}" alt="{product_name}"
                        style="width:100%;aspect-ratio:3/4;object-fit:cover;
                        border-radius:4px;border:1px solid var(--border);
                        background:var(--card-bg);" />
                    """, unsafe_allow_html=True)
                else:
                    # Fallback kalau produk belum punya URL gambar di database.
                    img_initial = product_name[0].upper() if product_name else "P"
                    st.markdown(f"""
                        <div style='aspect-ratio:3/4;background:var(--card-bg);
                        display:flex;align-items:center;justify-content:center;
                        font-family:"Cormorant Garamond",serif;font-style:italic;
                        color:var(--gold-light);font-size:1.5rem;border-radius:4px;border:1px solid var(--border)'>
                            {img_initial}
                        </div>
                    """, unsafe_allow_html=True)

            with c2:
                cat_name = MOCK_CATEGORIES.get(category_id, "Unknown Category")
                st.markdown(f"""
                    <div style='font-size:0.62rem;letter-spacing:0.25em;
                    text-transform:uppercase;color:var(--gold);margin-bottom:0.3rem'>
                        {cat_name}
                    </div>
                    <div style='font-family:"Cormorant Garamond",serif;font-size:1.1rem;
                    margin-bottom:0.8rem;color:var(--text)'>
                        {product_name}
                    </div>
                """, unsafe_allow_html=True)


                new_qty = st.number_input(
                    label="Quantity",
                    min_value=1,
                    max_value=10,
                    value=int(item["qty"]),
                    key=f"qty_{item['cart_id']}",
                    label_visibility="collapsed",
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
                current_qty = st.session_state.get(f"qty_{cart_id}", qty)
                st.markdown(f"""
                    <div style='font-size:1rem;font-weight:500;text-align:right;padding-top:0.5rem;color:var(--text)'>
                       {format_price(price * current_qty)}
                    </div>
                """, unsafe_allow_html=True)

            st.divider()

    with col_summary:
        subtotal = sum(
            i.get("price", 0) * st.session_state.get(f"qty_{i.get('cart_id')}", i.get("qty", 1))
            for i in cart
        )
        shipping = 0 if subtotal >= 500000 else 45000
        total = subtotal + shipping

        st.markdown(f"""
            <div style='border:1px solid var(--border);padding:1.5rem;background:var(--card-bg)'>
                <div style='font-family:"Cormorant Garamond",serif;font-size:1.5rem;
                margin-bottom:1.5rem;padding-bottom:1rem;
                border-bottom:1px solid var(--border);color:var(--text)'>
                    Order Summary
                </div>
                <div style='display:flex;justify-content:space-between;
                font-size:0.82rem;color:var(--text-muted);margin-bottom:0.8rem'>
                    <span>Subtotal</span><span>{format_price(subtotal)}</span>
                </div>
                <div style='display:flex;justify-content:space-between;
                font-size:0.82rem;color:var(--text-muted);margin-bottom:0.8rem'>
                    <span>Shipping</span>
                    <span>{'Free' if shipping == 0 else format_price(shipping)}</span>
                </div>
                <div style='display:flex;justify-content:space-between;
                font-size:1rem;font-weight:500;padding-top:1rem;
                border-top:1px solid var(--border);color:var(--text)'>
                    <span>Total</span><span>{format_price(total)}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.session_state["checkout_total"] = subtotal
        st.session_state["checkout_cart"] = cart

        if st.button("Proceed to Checkout →", use_container_width=True):
            st.switch_page("pages/4_Checkout.py")


