import streamlit as st
from utils.session import init_session
from utils.mock_data import MOCK_PRODUCTS_SAMPLE, MOCK_CATEGORIES

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
        <span style='font-size:0.68rem;letter-spacing:0.35em;text-transform:uppercase;color:#C9A96E'>Discover</span>
        <h1 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:2.5rem'>
            Our <em style='color:#C9A96E'>Collection</em>
        </h1>
        <div style='width:40px;height:1px;background:#C9A96E;margin-top:0.8rem;margin-bottom:2rem'></div>
    </div>
""", unsafe_allow_html=True)

# Layout: Kolom Kiri (Filter), Kolom Kanan (Grid Produk)
col_filter, col_products = st.columns([1, 3])

with col_filter:
    st.markdown("<h4 style='font-family:\"Cormorant Garamond\",serif;'>Filter</h4>", unsafe_allow_html=True)
    
    # Pencarian
    search_query = st.text_input("Cari Produk", placeholder="Nama produk...").lower()
    
    # Filter Kategori
    kategori_options = ["Semua"] + list(MOCK_CATEGORIES.values())
    selected_category = st.radio("Kategori", options=kategori_options)
    
    # Filter Harga
    st.markdown("<br><b>Urutkan Berdasarkan</b>", unsafe_allow_html=True)
    sort_option = st.selectbox(
        "Urutkan", 
        options=["Rekomendasi", "Harga: Rendah ke Tinggi", "Harga: Tinggi ke Rendah"],
        label_visibility="collapsed"
    )

with col_products:
    # Memfilter data produk
    filtered_products = MOCK_PRODUCTS_SAMPLE
    
    # Filter by Search
    if search_query:
        filtered_products = [p for p in filtered_products if search_query in p.get("product_name", "").lower() or search_query in p.get("description", "").lower()]
        
    # Filter by Category
    if selected_category != "Semua":
        cat_id = next((k for k, v in MOCK_CATEGORIES.items() if v == selected_category), None)
        if cat_id:
            filtered_products = [p for p in filtered_products if p.get("category_id") == cat_id]
            
    # Sort Products
    if sort_option == "Harga: Rendah ke Tinggi":
        filtered_products = sorted(filtered_products, key=lambda x: x.get("price", 0))
    elif sort_option == "Harga: Tinggi ke Rendah":
        filtered_products = sorted(filtered_products, key=lambda x: x.get("price", 0), reverse=True)

    # Render Grid Produk
    if not filtered_products:
        st.info("Tidak ada produk yang cocok dengan kriteria pencarian Anda.")
    else:
        # MEMANGGIL FUNGSI ANDA: 
        # Kita menggunakan 2 kolom saja karena desain card Anda (kiri gambar, kanan teks) lumayan lebar
        product_grid(filtered_products, columns=2)
