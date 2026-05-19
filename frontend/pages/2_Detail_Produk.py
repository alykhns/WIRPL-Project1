import streamlit as st
from utils.session import init_session, is_logged_in
from utils.api_client import add_to_cart
from utils.formatter import format_price
from utils.mock_data import MOCK_PRODUCTS_SAMPLE
from components.style import inject_style
from components.navbar import render_navbar
from components.toast import show_success, show_error

st.set_page_config(page_title="Detail Produk - Lumière", page_icon="✨", layout="wide")

inject_style()
init_session()
render_navbar()

# Mendapatkan ID produk dari Session State atau URL param (di sini menggunakan session state sebagai state manager)
product_id = st.session_state.get("selected_product_id")

if not product_id:
    st.warning("Pilih produk dari halaman Katalog terlebih dahulu.")
    if st.button("Kembali ke Katalog"):
        st.switch_page("pages/1_Katalog.py")
    st.stop()

# Mencari data produk berdasarkan ID
product = next((p for p in MOCK_PRODUCTS_SAMPLE if p.get("product_id") == product_id), None)

if not product:
    st.error("Produk tidak ditemukan.")
    st.stop()

# Layout Detail Produk
if st.button("← Kembali ke Katalog"):
    st.switch_page("pages/1_Katalog.py")

st.markdown("<br>", unsafe_allow_html=True)

col_image, col_info = st.columns([1, 1.2])

with col_image:
    # Menggunakan placeholder gambar jika tidak ada URL gambar asli
    image_url = product.get("image_url", "https://via.placeholder.com/600x600.png?text=Lumière+Product")
    st.image(image_url, use_container_width=True)

with col_info:
    st.markdown(f"""
        <h1 style='font-family:"Cormorant Garamond",serif;font-weight:400;margin-bottom:0;'>
            {product.get('product_name', 'Nama Produk')}
        </h1>
        <h3 style='color:#C9A96E; margin-top:0.5rem;'>{format_price(product.get('price', 0))}</h3>
        <hr style='border:0.5px solid #EAEAEA;'>
    """, unsafe_allow_html=True)
    
    st.write("**Deskripsi Produk:**")
    st.write(product.get('description', 'Tidak ada deskripsi tersedia untuk produk ini.'))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Input Kuantitas
    qty = st.number_input("Kuantitas", min_value=1, max_value=product.get('inventory_count', 10), value=1)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action Buttons
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🛒 Tambah ke Keranjang", use_container_width=True, type="primary"):
            if not is_logged_in():
                show_error("Silakan login terlebih dahulu untuk berbelanja.")
            else:
                success = add_to_cart(product_id, qty)
                if success:
                    show_success(f"{qty} {product.get('product_name')} ditambahkan ke keranjang!")
                else:
                    show_error("Gagal menambahkan ke keranjang.")
    
    with c2:
        if st.button("💳 Beli Langsung", use_container_width=True):
            if not is_logged_in():
                show_error("Silakan login terlebih dahulu.")
            else:
                # Bypass langsung ke checkout membawa 1 item ini
                st.session_state["checkout_cart"] = [{
                    "product_id": product_id,
                    "product_name": product.get('product_name'),
                    "price": product.get('price'),
                    "qty": qty
                }]
                st.session_state["checkout_total"] = product.get('price', 0) * qty
                st.session_state.checkout_step = 1
                st.switch_page("pages/4_Checkout.py")
