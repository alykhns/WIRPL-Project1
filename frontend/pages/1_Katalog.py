import streamlit as st
from utils.session import init_session
from utils.api_client import get_products, get_categories

# IMPORT YANG BENAR: Mengambil fungsi product_grid dari file Anda
from components.product_card import product_grid 

from components.style import inject_style
from components.navbar import render_navbar

# Konfigurasi Halaman
st.set_page_config(page_title="Katalog Produk - Lumière", page_icon="🛍️", layout="wide")

# Inisialisasi
inject_style()
init_session()
render_navbar()

# Header
st.markdown("""
    <div style='padding: 2rem 0 1rem'>
        <span style='font-size:0.68rem;letter-spacing:0.35em;text-transform:uppercase;color:var(--gold)'>Discover</span>
        <h1 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:2.5rem;color:var(--text)'>
            Our <em style='color:var(--gold)'>Collection</em>
        </h1>
        <div style='width:40px;height:1px;background:var(--gold);margin-top:0.8rem;margin-bottom:2rem'></div>
    </div>
""", unsafe_allow_html=True)

# Layout: Kolom Kiri (Filter), Kolom Kanan (Grid Produk)
col_filter, col_products = st.columns([1, 3])

with col_filter:
    st.markdown("<h4 style='font-family:\"Cormorant Garamond\",serif;color:var(--text);'>Filter</h4>", unsafe_allow_html=True)
    
    # Pencarian
    search_query = st.text_input("Cari Produk", placeholder="Nama produk...")
    
    # Filter Kategori
    categories = get_categories()
    kategori_options = ["Semua"] + [c["category_name"] for c in categories]
    selected_category = st.radio("Kategori", options=kategori_options)
    
    # Filter Harga
    st.markdown("<br><b>Urutkan Berdasarkan</b>", unsafe_allow_html=True)
    sort_option = st.selectbox(
        "Urutkan", 
        options=["Rekomendasi", "Harga: Rendah ke Tinggi", "Harga: Tinggi ke Rendah"],
        label_visibility="collapsed"
    )

with col_products:
    # Map sort option to api_client sort_by
    sort_by = "newest"
    if sort_option == "Harga: Rendah ke Tinggi":
        sort_by = "price_asc"
    elif sort_option == "Harga: Tinggi ke Rendah":
        sort_by = "price_desc"
        
    # Get Category ID
    cat_id = None
    if selected_category != "Semua":
        cat_id = next((c["category_id"] for c in categories if c["category_name"] == selected_category), None)

    # Fetch from API
    filtered_products = get_products(
        search=search_query,
        category_id=cat_id,
        sort_by=sort_by
    )

    # Render Grid Produk
    if not filtered_products:
        st.info("Tidak ada produk yang cocok dengan kriteria pencarian Anda.")
    else:
        # MEMANGGIL FUNGSI ANDA: 
        # Kita menggunakan 2 kolom saja karena desain card Anda (kiri gambar, kanan teks) lumayan lebar
        product_grid(filtered_products, columns=2)
