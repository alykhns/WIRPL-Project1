import streamlit as st
from components.style import inject_style
from components.product_card import inject_card_style, render_product_grid
from utils.api_client import (
    get_product_by_id, get_products, add_to_cart,
)
from utils.mock_data import MOCK_CATEGORIES

st.set_page_config(
    page_title="Detail Produk — Lumière",
    page_icon="◇",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_style()
inject_card_style()

# ============================================================
# READ PRODUCT ID DARI URL
# ============================================================
qp = st.query_params
pid = qp.get("id")

# ============================================================
# EMPTY STATE — kalau user buka /Detail_Produk dari navbar (tanpa id)
# ============================================================
if not pid:
    st.markdown("""
        <style>
        .lum-empty-detail {
            text-align: center;
            padding: 6rem 1rem;
        }
        .lum-empty-detail h1 {
            font-family: 'Cormorant Garamond', serif;
            font-size: 2.4rem; font-weight: 300; color: #1A1A1A;
            margin-bottom: 0.8rem;
        }
        .lum-empty-detail h1 em { font-style: italic; color: #8B6914; }
        .lum-empty-detail p {
            color: #8A8476; font-size: 0.95rem; max-width: 480px;
            margin: 0 auto 2rem; line-height: 1.7;
        }
        .lum-empty-cta {
            display: inline-block;
            font-size: 0.72rem; letter-spacing: 0.22em; text-transform: uppercase;
            color: #1A1A1A; text-decoration: none;
            padding: 12px 32px; border: 1px solid #1A1A1A;
            transition: all 0.25s;
        }
        .lum-empty-cta:hover { background: #1A1A1A; color: #FAF7F2; }
        </style>
        <div class="lum-empty-detail">
            <h1>Pilih dulu <em>produk</em></h1>
            <p>Halaman ini menampilkan detail untuk satu produk. Buka katalog
               dan pilih item yang ingin kamu lihat lebih dekat.</p>
            <a class="lum-empty-cta" href="/Katalog">Buka Katalog</a>
        </div>
    """, unsafe_allow_html=True)
    st.stop()


try:
    pid = int(pid)
except (TypeError, ValueError):
    st.error("ID produk tidak valid.")
    st.stop()

product = get_product_by_id(pid)
if not product:
    st.error("Produk tidak ditemukan.")
    st.markdown('<a href="/Katalog">← Kembali ke Katalog</a>',
                unsafe_allow_html=True)
    st.stop()


# ============================================================
# STYLING DETAIL PAGE
# ============================================================
st.markdown("""
    <style>
    .lum-breadcrumb {
        font-size: 0.65rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #8A8476;
        margin-bottom: 2rem;
        padding-top: 0.5rem;
    }
    .lum-breadcrumb a {
        color: #8A8476; text-decoration: none;
        transition: color 0.2s;
    }
    .lum-breadcrumb a:hover { color: #1A1A1A; }
    .lum-breadcrumb .sep { margin: 0 0.6rem; color: #C9A96E; }

    .lum-detail-img-wrap {
        width: 100%;
        aspect-ratio: 4/5;
        overflow: hidden;
        background: linear-gradient(135deg, #E8D5B0 0%, #FAF7F2 100%);
    }
    .lum-detail-img-wrap img {
        width: 100%; height: 100%; object-fit: cover;
    }

    .lum-detail-eyebrow {
        font-size: 0.7rem; letter-spacing: 0.28em;
        text-transform: uppercase; color: #C9A96E;
        margin-bottom: 0.8rem;
    }
    .lum-detail-brand {
        font-size: 0.75rem; letter-spacing: 0.25em;
        text-transform: uppercase; color: #8A8476;
        margin-bottom: 0.6rem;
    }
    .lum-detail-name {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.6rem; font-weight: 300; line-height: 1.1;
        color: #1A1A1A; margin: 0 0 1.2rem;
    }
    .lum-detail-name em { font-style: italic; color: #8B6914; }
    .lum-detail-price {
        font-size: 1.5rem; color: #1A1A1A;
        letter-spacing: 0.04em; margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid rgba(201,169,110,0.25);
    }

    .lum-spec-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.9rem 1.5rem;
        margin: 1.5rem 0 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid rgba(201,169,110,0.25);
    }
    .lum-spec-label {
        font-size: 0.62rem; letter-spacing: 0.24em;
        text-transform: uppercase; color: #8A8476;
        margin-bottom: 0.2rem;
    }
    .lum-spec-value {
        font-size: 0.95rem; color: #1A1A1A;
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
    }

    .lum-desc {
        font-size: 0.92rem; line-height: 1.75;
        color: #2D2D2D; margin: 1rem 0 1.8rem;
    }

    .lum-stock {
        font-size: 0.7rem; letter-spacing: 0.22em;
        text-transform: uppercase; margin-bottom: 1.2rem;
    }
    .lum-stock.in    { color: #27AE60; }
    .lum-stock.low   { color: #8B6914; }
    .lum-stock.out   { color: #C0392B; }

    /* tombol Add to Cart custom (st.button) */
    .stButton button {
        background: #1A1A1A !important;
        color: #FAF7F2 !important;
        border: 1px solid #1A1A1A !important;
        border-radius: 0 !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.24em !important;
        text-transform: uppercase !important;
        padding: 14px 0 !important;
        font-family: 'Jost', sans-serif !important;
        width: 100%;
    }
    .stButton button:hover {
        background: #C9A96E !important;
        color: white !important;
        border-color: #C9A96E !important;
    }
    .stButton button:disabled {
        background: #8A8476 !important;
        border-color: #8A8476 !important;
        cursor: not-allowed !important;
    }

    /* number input styling */
    .stNumberInput label {
        font-size: 0.66rem !important;
        letter-spacing: 0.22em !important;
        text-transform: uppercase !important;
        color: #8A8476 !important;
    }
    .stNumberInput input {
        background: #FAF7F2 !important;
        border-radius: 0 !important;
    }

    .lum-section-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem; font-weight: 300;
        text-align: center; color: #1A1A1A;
        margin: 5rem 0 0.3rem;
    }
    .lum-section-sub {
        text-align: center;
        font-size: 0.72rem; letter-spacing: 0.28em;
        text-transform: uppercase; color: #C9A96E;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================
# BREADCRUMB
# ============================================================
cat_name = MOCK_CATEGORIES.get(product["category_id"], "Collection")
st.markdown(f"""
    <div class="lum-breadcrumb">
        <a href="/">Home</a> <span class="sep">/</span>
        <a href="/Katalog?category={product['category_id']}">{cat_name}</a>
        <span class="sep">/</span>
        <span>{product['product_name']}</span>
    </div>
""", unsafe_allow_html=True)


# ============================================================
# LAYOUT: GAMBAR (kiri) + INFO (kanan)
# ============================================================
col_img, col_info = st.columns([1, 1], gap="large")

with col_img:
    st.markdown(f"""
        <div class="lum-detail-img-wrap">
            <img src="{product['image_url']}" alt="{product['product_name']}" />
        </div>
    """, unsafe_allow_html=True)

with col_info:
    st.markdown(f"""
        <div class="lum-detail-eyebrow">— {cat_name} —</div>
        <div class="lum-detail-brand">{product['brand']}</div>
        <h1 class="lum-detail-name">{product['product_name']}</h1>
        <div class="lum-detail-price">${product['price']:,.2f}</div>
    """, unsafe_allow_html=True)

    st.markdown(f"<p class='lum-desc'>{product['description']}</p>",
                unsafe_allow_html=True)

    # spec
    st.markdown(f"""
        <div class="lum-spec-grid">
            <div>
                <div class="lum-spec-label">Color</div>
                <div class="lum-spec-value">{product['color']}</div>
            </div>
            <div>
                <div class="lum-spec-label">Size</div>
                <div class="lum-spec-value">{product['size']}</div>
            </div>
            <div>
                <div class="lum-spec-label">Material</div>
                <div class="lum-spec-value">{product['material'].title()}</div>
            </div>
            <div>
                <div class="lum-spec-label">Season</div>
                <div class="lum-spec-value">{product['season'].title()}</div>
            </div>
            <div>
                <div class="lum-spec-label">Style</div>
                <div class="lum-spec-value">{product['style'].title()}</div>
            </div>
            <div>
                <div class="lum-spec-label">SKU</div>
                <div class="lum-spec-value">LUM-{product['product_id']:04d}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # stock indicator
    stock = product["inventory_count"]
    if stock == 0:
        stock_class, stock_msg = "out", "Out of Stock"
    elif stock < 20:
        stock_class, stock_msg = "low", f"Only {stock} left — order soon"
    else:
        stock_class, stock_msg = "in", "In Stock"

    st.markdown(
        f"<div class='lum-stock {stock_class}'>◆ {stock_msg}</div>",
        unsafe_allow_html=True,
    )

    # qty + add to cart
    q_col, b_col = st.columns([1, 2])
    with q_col:
        qty = st.number_input(
            "Qty", min_value=1,
            max_value=max(stock, 1),
            value=1, step=1,
            key=f"qty_{pid}",
            label_visibility="visible",
        )
    with b_col:
        st.markdown("<div style='height: 1.55rem'></div>",
                    unsafe_allow_html=True)
        if st.button("◇  Add to Cart",
                     disabled=(stock == 0),
                     key=f"add_{pid}"):
            result = add_to_cart(product["product_id"], int(qty))
            if result:
                st.success(
                    f"✓ {product['product_name']} ditambahkan ke keranjang."
                )
            else:
                st.error("Gagal menambahkan ke keranjang.")


# ============================================================
# RELATED PRODUCTS (kategori sama, exclude diri sendiri)
# ============================================================
st.markdown("""
    <h2 class="lum-section-title">You May Also Love</h2>
    <div class="lum-section-sub">— Curated for You —</div>
""", unsafe_allow_html=True)

related = [
    p for p in get_products(category_id=product["category_id"], limit=20)
    if p["product_id"] != product["product_id"]
][:4]
render_product_grid(related)