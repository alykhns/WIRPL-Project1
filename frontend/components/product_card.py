import streamlit as st
from utils.mock_data import MOCK_CATEGORIES


def inject_card_style():
    """Sekali inject di tiap page yang pakai product card."""
    st.markdown("""
        <style>
        .lum-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 2rem 1.5rem;
            margin-top: 1.5rem;
        }
        .lum-card {
            background: #FAF7F2;
            border: 1px solid rgba(201,169,110,0.18);
            display: flex;
            flex-direction: column;
            text-decoration: none;
            color: inherit;
            transition: all 0.25s ease;
        }
        .lum-card:hover {
            border-color: rgba(201,169,110,0.55);
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(26,26,26,0.06);
        }
        .lum-card-img-wrap {
            position: relative;
            width: 100%;
            aspect-ratio: 4 / 5;
            overflow: hidden;
            background: linear-gradient(135deg, #E8D5B0 0%, #FAF7F2 100%);
        }
        .lum-card-img {
            width: 100%; height: 100%;
            object-fit: cover;
            transition: transform 0.4s ease;
        }
        .lum-card:hover .lum-card-img { transform: scale(1.04); }

        .lum-card-cat {
            position: absolute;
            top: 12px; left: 12px;
            background: rgba(250,247,242,0.92);
            backdrop-filter: blur(6px);
            color: #8B6914;
            font-size: 0.62rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            padding: 4px 10px;
        }

        .lum-card-body { padding: 1rem 0.9rem 1.2rem; }
        .lum-card-brand {
            font-size: 0.66rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: #8A8476;
            margin-bottom: 0.35rem;
        }
        .lum-card-name {
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.15rem;
            font-weight: 400;
            color: #1A1A1A;
            margin-bottom: 0.55rem;
            line-height: 1.3;
        }
        .lum-card-price {
            font-family: 'Jost', sans-serif;
            font-size: 0.95rem;
            color: #1A1A1A;
            letter-spacing: 0.04em;
        }
        .lum-card-meta {
            display: flex;
            gap: 0.6rem;
            margin-top: 0.5rem;
            font-size: 0.65rem;
            color: #8A8476;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        .lum-card-meta span { display: inline-block; }
        .lum-card-meta span + span:before {
            content: "·"; margin-right: 0.6rem; color: #C9A96E;
        }
        </style>
    """, unsafe_allow_html=True)


def _format_price(price: float) -> str:
    """Format harga ke USD biar konsisten dengan data."""
    return f"${price:,.2f}"


def render_card_html(product: dict) -> str:
    pid = product["product_id"]
    cat = MOCK_CATEGORIES.get(product["category_id"], "")
    img = product['image_url']
    name = product['product_name']
    brand = product['brand']
    price = _format_price(product['price'])
    color = product['color']
    size = product['size']
    season = product['season'].title()

    return (
        f'<a class="lum-card" href="/Detail_Produk?id={pid}" target="_self">'
        f'<div class="lum-card-img-wrap">'
        f'<span class="lum-card-cat">{cat}</span>'
        f'<img class="lum-card-img" src="{img}" alt="{name}" loading="lazy" />'
        f'</div>'
        f'<div class="lum-card-body">'
        f'<div class="lum-card-brand">{brand}</div>'
        f'<div class="lum-card-name">{name}</div>'
        f'<div class="lum-card-price">{price}</div>'
        f'<div class="lum-card-meta">'
        f'<span>{color}</span><span>{size}</span><span>{season}</span>'
        f'</div>'
        f'</div>'
        f'</a>'
    )


def render_product_grid(products: list[dict]):
    if not products:
        st.markdown("""
            <div style="text-align:center;padding:4rem 1rem;color:#8A8476;
                        font-family:'Cormorant Garamond',serif;font-size:1.3rem;
                        font-style:italic;">
                Tidak ada produk yang sesuai dengan filtermu.
            </div>
        """, unsafe_allow_html=True)
        return

    cards_html = "".join(render_card_html(p) for p in products)
    
    cards_html = cards_html.replace("\xa0", " ").replace("\n", " ").replace("\t", " ")
    
    grid_html = f'<div class="lum-grid">{cards_html}</div>'
    st.markdown(grid_html, unsafe_allow_html=True)