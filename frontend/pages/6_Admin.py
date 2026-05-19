import streamlit as st
import pandas as pd
from datetime import datetime

from utils.session import is_logged_in, logout, init_session
from utils.api_client import (
    get_profile, get_admin_stats, get_admin_orders, admin_update_order_status,
    get_products, create_product, update_product, delete_product, get_categories
)
from utils.formatter import format_price, get_status_color, get_status_bg
from components.style import inject_style
from components.navbar import render_navbar

st.set_page_config(page_title="Admin - Lumière", page_icon="⚙️", layout="wide", initial_sidebar_state="expanded")

init_session()
inject_style()
render_navbar()

# Bypass Otorisasi Admin untuk Keperluan Pengembangan/Testing
IS_ADMIN = True
user = {}
membership_level = "Admin (Dev Mode)"

st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-family: 'Cormorant Garamond', serif; color: var(--gold); margin: 0;">
            ⚙️ ADMIN DASHBOARD
        </h1>
        <p style="color: var(--text-muted); margin-top: 0.5rem;">Lumière Management System</p>
    </div>
""", unsafe_allow_html=True)
st.markdown("<hr style='border-top: 1px solid var(--hr);'>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard", "📦 Products", "📁 Categories", "📋 Orders"
])

# TAB 1: DASHBOARD
with tab1:
    stats = get_admin_stats()
    st.subheader("Ringkasan Sistem")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Pesanan", stats.get("total_orders", 0))
    with col2: st.metric("Total Pendapatan", format_price(stats.get("total_revenue", 0)))
    with col3: st.metric("Total Produk", stats.get("total_products", 0))
    with col4: st.metric("Kategori Aktif", stats.get("active_categories", 0))
    
    st.markdown("<hr style='border-top: 1px solid var(--hr);'>", unsafe_allow_html=True)
    orders = get_admin_orders()
    if orders:
        st.subheader("Pesanan Terbaru")
        for order in orders[:5]:
            status = order.get("status", "pending")
            sc = get_status_color(status)
            sb = get_status_bg(status)
            st.markdown(f"""
                <div style="padding: 1rem; border-radius: 8px; border-left: 4px solid {sc}; background: {sb}; margin-bottom: 0.5rem;">
                    <p style="margin: 0; font-weight: bold; color: var(--text);">Order #{order.get('order_id')} - {format_price(order.get('total_amount', 0))}</p>
                    <p style="margin: 0; font-size: 0.8rem; color: {sc};">{status.upper()}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Belum ada pesanan terbaru.")

# TAB 2: PRODUCTS
with tab2:
    st.subheader("Manajemen Produk")
    
    with st.expander("➕ Tambah Produk Baru"):
        with st.form("add_product_form"):
            name = st.text_input("Nama Produk")
            desc = st.text_area("Deskripsi")
            price = st.number_input("Harga", min_value=0, step=1000)
            stock = st.number_input("Stok", min_value=0, step=1)
            image = st.file_uploader("Gambar Produk", type=["jpg", "png", "jpeg"])
            
            submit = st.form_submit_button("Simpan Produk")
            if submit:
                if name and price and image:
                    data = {"name": name, "description": desc, "price": price, "stock": stock}
                    files = {"image": (image.name, image.getvalue(), image.type)}
                    res = create_product(data, files)
                    if res:
                        st.success("Produk berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("Gagal menambahkan produk.")
                else:
                    st.warning("Mohon isi semua field wajib (Nama, Harga, Gambar).")

    st.markdown("<hr style='border-top: 1px solid var(--hr);'>", unsafe_allow_html=True)
    products = get_products()
    if products:
        for p in products:
            col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
            with col1:
                if p.get("image_url"):
                    st.image(p["image_url"], width=80)
                else:
                    st.markdown(f"<div style='width:80px;height:80px;background:var(--card-bg);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;color:var(--text-muted);'>No Image</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='color:var(--text);font-weight:bold;'>{p['name']}</div>", unsafe_allow_html=True)
                st.caption(p.get('description', '')[:100] + "...")
            with col3:
                st.markdown(f"<div style='color:var(--text);'>{format_price(p['price'])}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color:var(--text-muted);font-size:0.8rem;'>Stok: {p['stock']}</div>", unsafe_allow_html=True)
            with col4:
                if st.button("🗑️ Hapus", key=f"del_{p['product_id']}"):
                    if delete_product(p['product_id']):
                        st.success("Dihapus!")
                        st.rerun()
                    else:
                        st.error("Gagal")
            st.markdown("<hr style='border-top: 1px solid var(--hr);'>", unsafe_allow_html=True)
    else:
        st.info("Belum ada produk.")

# TAB 3: CATEGORIES
with tab3:
    st.subheader("Kategori Produk")
    categories = get_categories()
    if categories:
        df_categories = pd.DataFrame(categories)
        st.dataframe(df_categories, use_container_width=True)
    else:
        st.info("Belum ada kategori.")

# TAB 4: ORDERS
with tab4:
    st.subheader("Manajemen Semua Pesanan")
    orders = get_admin_orders()
    
    if orders:
        for order in orders:
            with st.container():
                c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
                order_id = order.get('order_id')
                current_status = order.get('status', 'pending')
                
                with c1:
                    st.markdown(f"<div style='color:var(--text);font-weight:bold;'>#{order_id}</div>", unsafe_allow_html=True)
                    st.caption(order.get('created_at', ''))
                with c2:
                    st.markdown(f"<div style='color:var(--text);'>Total: {format_price(order.get('total_amount', 0))}</div>", unsafe_allow_html=True)
                    st.caption(f"Customer ID: {order.get('customer_id')}")
                with c3:
                    new_status = st.selectbox(
                        "Update Status",
                        options=["pending", "processing", "shipped", "delivered", "cancelled"],
                        index=["pending", "processing", "shipped", "delivered", "cancelled"].index(current_status) if current_status in ["pending", "processing", "shipped", "delivered", "cancelled"] else 0,
                        key=f"status_{order_id}"
                    )
                with c4:
                    if st.button("Update", key=f"btn_{order_id}"):
                        if admin_update_order_status(order_id, new_status):
                            st.success("Updated!")
                            st.rerun()
                        else:
                            st.error("Failed")
                st.markdown("<hr style='border-top: 1px solid var(--hr);'>", unsafe_allow_html=True)
    else:
        st.info("Belum ada pesanan.")
