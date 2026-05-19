import streamlit as st
import pandas as pd
from datetime import datetime

from utils.session import is_logged_in, logout, init_session
from utils.api_client import get_profile, get_order_history
from utils.formatter import format_price, get_status_color, get_status_bg
from utils.mock_data import MOCK_USER, MOCK_ORDERS, MOCK_PRODUCTS_SAMPLE, MOCK_CATEGORIES
from components.style import inject_style
from components.navbar import render_navbar

st.set_page_config(page_title="Admin - Lumière", page_icon="⚙️", layout="wide", initial_sidebar_state="expanded")

init_session()
inject_style()
render_navbar()

# Cek Otorisasi Admin
user = get_profile()
membership_level = user.get('membership_level', '').lower()

if not is_logged_in() or membership_level not in ['platinum', 'admin']:
    st.error("❌ Akses Ditolak: Halaman Admin hanya untuk pengguna yang memiliki otoritas.")
    st.info("Silakan login dengan akun bersatus Admin/Platinum.")
    st.stop()

st.markdown("---")
st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-family: 'Cormorant Garamond', serif; color: #C9A96E; margin: 0;">
            ⚙️ ADMIN DASHBOARD
        </h1>
        <p style="color: #8A8476; margin-top: 0.5rem;">Lumière Management System</p>
    </div>
""", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard", "📦 Products", "📁 Categories", "📋 Orders", "📈 Reports"
])

# TAB 1: DASHBOARD
with tab1:
    st.subheader("Ringkasan Sistem")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Pesanan", len(MOCK_ORDERS), "+5 minggu ini")
    with col2: st.metric("Total Pendapatan", format_price(sum([o["total"] for o in MOCK_ORDERS])), "+12.5%")
    with col3: st.metric("Total Produk", len(MOCK_PRODUCTS_SAMPLE), "+2 produk baru")
    with col4: st.metric("Kategori", len(MOCK_CATEGORIES), "Aktif")
    
    st.markdown("---")
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Distribusi Status Pesanan")
        status_counts = {}
        for o in MOCK_ORDERS:
            s = o.get("status", "unknown")
            status_counts[s] = status_counts.get(s, 0) + 1
        if status_counts:
            st.bar_chart(pd.DataFrame({"Jumlah": list(status_counts.values())}, index=list(status_counts.keys())))
            
    with col_right:
        st.subheader("Pesanan Terbaru")
        for order in sorted(MOCK_ORDERS, key=lambda x: x["date"], reverse=True)[:4]:
            sc = get_status_color(order["status"])
            sb = get_status_bg(order["status"])
            st.markdown(f"""
                <div style="padding: 1rem; border-radius: 8px; border-left: 4px solid {sc}; background: {sb}; margin-bottom: 0.5rem;">
                    <p style="margin: 0; font-weight: bold;">Order #{order['order_id']} - {format_price(order['total'])}</p>
                    <p style="margin: 0; font-size: 0.8rem; color: {sc};">{order['status'].upper()}</p>
                </div>
            """, unsafe_allow_html=True)

# TAB 2: PRODUCTS
with tab2:
    st.subheader("Manajemen Produk")
    df_products = pd.DataFrame(MOCK_PRODUCTS_SAMPLE)
    if not df_products.empty:
        st.dataframe(df_products[["product_id", "product_name", "category_id", "price", "inventory_count"]], use_container_width=True)

# TAB 3: CATEGORIES
with tab3:
    st.subheader("Kategori Produk")
    df_categories = pd.DataFrame(list(MOCK_CATEGORIES.items()), columns=["Category ID", "Category Name"])
    st.dataframe(df_categories, use_container_width=True)

# TAB 4: ORDERS
with tab4:
    st.subheader("Daftar Semua Pesanan")
    df_orders = pd.DataFrame(MOCK_ORDERS)
    if not df_orders.empty:
        st.dataframe(df_orders[["order_id", "date", "status", "total"]], use_container_width=True)

# TAB 5: REPORTS
with tab5:
    st.subheader("Laporan Penjualan")
    report_type = st.selectbox("Pilih Jenis Laporan", options=["Ringkasan Penjualan", "Status Inventaris Data"])
    st.markdown("---")
    
    if report_type == "Ringkasan Penjualan":
        status_summary = {}
        for o in MOCK_ORDERS:
            status_summary[o["status"]] = status_summary.get(o["status"], 0) + o["total"]
        st.bar_chart(pd.DataFrame({"Pendapatan (Rp)": list(status_summary.values())}, index=list(status_summary.keys())))
        
    elif report_type == "Status Inventaris Data":
        st.write("**Tingkat Stok Saat Ini**")
        inv_data = []
        for p in MOCK_PRODUCTS_SAMPLE:
            stock = p.get("inventory_count", 0)
            status = "✓ Aman" if stock > 50 else "⚠️ Menipis" if stock > 10 else "✗ Kritis"
            inv_data.append({"Produk": p.get("product_name"), "Sisa Stok": stock, "Status": status})
        st.dataframe(pd.DataFrame(inv_data), use_container_width=True)