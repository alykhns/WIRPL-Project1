import streamlit as st

# Konfigurasi Halaman - HARUS DI ATAS
st.set_page_config(
    page_title="Lumière - Luxury Fashion",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from components.navbar import render_navbar
from utils.api_client import login, register
from utils.session import is_logged_in, init_session
from components.toast import show_success, show_error
from components.style import inject_style

init_session()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

inject_style()
render_navbar()



# hero
st.markdown("""
    <style>
    .lumiere-hero {
        background: var(--hero-bg);
        padding: 6rem 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin: -1rem -1rem 2rem -1rem;
    }
    .lumiere-hero::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at 50% 40%, rgba(201,169,110,0.10) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-label {
        font-size: 0.68rem;
        letter-spacing: 0.45em;
        text-transform: uppercase;
        color: var(--gold);
        display: block;
        margin-bottom: 1.5rem;
        font-family: 'Jost', sans-serif;
    }
    .hero-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(3rem, 8vw, 5.5rem);
        font-weight: 300;
        color: var(--hero-text);
        line-height: 1.05;
        letter-spacing: 0.04em;
        margin-bottom: 1.5rem;
    }
    .hero-title em {
        color: var(--gold);
        font-style: italic;
    }
    .hero-desc {
        font-size: 0.88rem;
        color: var(--text-muted);
        letter-spacing: 0.08em;
        max-width: 380px;
        margin: 0 auto 2.5rem auto !important;
        line-height: 1.7;
        font-family: 'Jost', sans-serif;
        text-align: center !important;
    }
    .hero-divider {
        width: 40px;
        height: 1px;
        background: var(--gold);
        margin: 0 auto 2.5rem;
    }
    .hero-ornament {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.5rem;
        color: rgba(201,169,110,0.3);
        letter-spacing: 0.6em;
        margin-bottom: 2rem;
    }
    </style>

    <div class="lumiere-hero">
        <span class="hero-label">New Collection · Spring 2026</span>
        <h1 class="hero-title">
            Where Fashion<br>Meets <em>Lumière</em>
        </h1>
        <div class="hero-divider"></div>
        <p class="hero-desc">
            Curated luxury fashion for those who seek the extraordinary in every detail.
        </p>
        <div class="hero-ornament">◇ &nbsp; ◇ &nbsp; ◇</div>
    </div>
""", unsafe_allow_html=True)

# cta
st.page_link("pages/1_Katalog.py", label="✦ Explore Collection")

st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

# stats
st.markdown("""
    <div style='display:flex;justify-content:center;gap:4rem;
    padding:2rem 0;border-top:1px solid var(--hr);
    border-bottom:1px solid var(--hr);margin-bottom:3rem'>
        <div style='text-align:center'>
            <div style='font-family:"Cormorant Garamond",serif;font-size:2rem;
            font-weight:300;color:var(--gold)'>500+</div>
            <div style='font-size:0.65rem;letter-spacing:0.25em;text-transform:uppercase;
            color:var(--text-muted);margin-top:0.3rem'>Curated Pieces</div>
        </div>
        <div style='text-align:center'>
            <div style='font-family:"Cormorant Garamond",serif;font-size:2rem;
            font-weight:300;color:var(--gold)'>12</div>
            <div style='font-size:0.65rem;letter-spacing:0.25em;text-transform:uppercase;
            color:var(--text-muted);margin-top:0.3rem'>Luxury Brands</div>
        </div>
        <div style='text-align:center'>
            <div style='font-family:"Cormorant Garamond",serif;font-size:2rem;
            font-weight:300;color:var(--gold)'>Free</div>
            <div style='font-size:0.65rem;letter-spacing:0.25em;text-transform:uppercase;
            color:var(--text-muted);margin-top:0.3rem'>Shipping ≥ 500K</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Join Us CTA
if not is_logged_in():
    st.markdown("""
        <div style='text-align:center;margin: 2rem 0 4rem'>
            <span style='font-size:0.68rem;letter-spacing:0.35em;text-transform:uppercase;color:var(--gold)'>Experience Luxury</span>
            <h2 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:2.2rem;margin-top:0.5rem;color:var(--text)'>
                Elevate Your <em style='color:var(--gold)'>Style</em>
            </h2>
            <p style='font-size:0.88rem;color:var(--text-muted);margin:1rem auto 2rem;max-width:500px;line-height:1.6'>
                Join Lumière to unlock exclusive collections, personalized recommendations, and premium membership benefits.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Sign In to Your Account", use_container_width=True):
        st.switch_page("pages/7_Login.py")
    
    st.markdown("<div style='margin-bottom: 4rem'></div>", unsafe_allow_html=True)
    st.markdown("---")

# categories
st.markdown("""
    <div style='text-align:center;margin-bottom:2rem'>
        <span style='font-size:0.68rem;letter-spacing:0.35em;text-transform:uppercase;
        color:var(--gold)'>Browse By</span>
        <h2 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:2rem;
        margin-top:0.3rem;color:var(--text)'>Category</h2>
        <div style='width:40px;height:1px;background:var(--gold);margin:0.8rem auto 0'></div>
    </div>
""", unsafe_allow_html=True)

categories = [
    ("Tops",       "◈", "Casual to formal, every occasion"),
    ("Dresses",    "◉", "Floral, maxi, evening & more"),
    ("Outerwear",  "◎", "Jackets, coats & cardigans"),
    ("Bottoms",    "◇", "Pants, skirts & trousers"),
    ("Accessories","◆", "Finishing touches that matter"),
]

cards_html = "".join(
    f'<div style="border:1px solid var(--border);padding:1.5rem 1rem;'
    f'text-align:center;background:var(--card-bg);display:flex;flex-direction:column;align-items:center;">'
    f'<div style="font-size:1.6rem;color:var(--gold);margin-bottom:0.8rem">{icon}</div>'
    f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:1rem;margin-bottom:0.4rem;color:var(--text)">{name}</div>'
    f'<div style="font-size:0.68rem;color:var(--text-muted);letter-spacing:0.05em;line-height:1.5">{desc}</div>'
    f'</div>'
    for name, icon, desc in categories
)

st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;">
        {cards_html}
    </div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:4rem'></div>", unsafe_allow_html=True)

# featured items
st.markdown("""
    <div style='text-align:center;margin-bottom:2rem'>
        <span style='font-size:0.68rem;letter-spacing:0.35em;text-transform:uppercase;
        color:var(--gold)'>Hand-Picked</span>
        <h2 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:2rem;
        margin-top:0.3rem;color:var(--text)'>Featured <em style="color:var(--gold)">Pieces</em></h2>
        <div style='width:40px;height:1px;background:var(--gold);margin:0.8rem auto 0'></div>
    </div>
""", unsafe_allow_html=True)

from utils.api_client import get_products, get_categories
from utils.formatter import format_price

# Fetch real products (limit to 3)
real_products = get_products(limit=3)
categories_list = get_categories()
categories_map = {c["category_id"]: c["category_name"] for c in categories_list}

if real_products:
    feat_cols = st.columns(3)
    for col, product in zip(feat_cols, real_products):
        with col:
            img_url = product.get("image_url", "")
            cat_name = categories_map.get(product.get("category_id"), "Luxury Piece")
            
            # Rendering image with fallback
            if img_url:
                img_html = f"<img src='{img_url}' style='width:100%;aspect-ratio:3/4;object-fit:cover;'>"
            else:
                initial = product["name"][0]
                img_html = f"""
                    <div style='aspect-ratio:3/4;background:var(--card-bg);
                    display:flex;align-items:center;justify-content:center;
                    font-family:"Cormorant Garamond",serif;font-style:italic;
                    color:var(--gold-light);font-size:4rem'>
                        {initial}
                    </div>
                """
                
            st.markdown(f"""
                <div style='border:1px solid var(--border);overflow:hidden;height:100%;background:var(--card-bg)'>
                    {img_html}
                    <div style='padding:1rem'>
                        <div style='font-size:0.62rem;letter-spacing:0.25em;text-transform:uppercase;
                        color:var(--gold);margin-bottom:0.3rem'>{cat_name}</div>
                        <div style='font-family:"Cormorant Garamond",serif;font-size:1.1rem;
                        margin-bottom:0.2rem;color:var(--text);font-weight:400'>{product["name"]}</div>
                        <div style='font-size:0.75rem;color:var(--text-muted);margin-bottom:0.8rem;height:2.5rem;overflow:hidden;'>
                            {product.get("description", "")[:60]}...
                        </div>
                        <div style='font-size:1rem;font-weight:600;color:var(--gold)'>
                            {format_price(product["price"])}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("No products available at the moment.")

st.markdown("<div style='margin-top:1.5rem;text-align:center'></div>", unsafe_allow_html=True)
st.page_link("pages/1_Katalog.py", label="View All Products →")

st.markdown("<div style='margin-top:3rem'></div>", unsafe_allow_html=True)

# membership banner
st.markdown("""
    <div style='background:var(--hero-bg);
    padding:3rem 2rem;text-align:center;
    border:1px solid var(--border);margin:2rem 0'>
        <span style='font-size:0.68rem;letter-spacing:0.45em;text-transform:uppercase;
        color:var(--gold)'>Exclusive Access</span>
        <h3 style='font-family:"Cormorant Garamond",serif;font-weight:300;
        font-size:2rem;color:var(--hero-text);margin:0.5rem 0'>
            Join <em style='color:var(--gold)'>Lumière</em> Membership
        </h3>
        <p style='font-size:0.85rem;color:var(--text-muted);
        max-width:400px;margin:0.8rem auto 0;line-height:1.7;letter-spacing:0.04em'>
            Unlock early access, free express shipping, and members-only collections.<br>
            Currently available: <strong style='color:var(--gold)'>Platinum</strong> tier for selected customers.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:3rem'></div>", unsafe_allow_html=True)

# footer
st.markdown("""
    <div style='text-align:center;padding:2rem 0;
    border-top:1px solid var(--hr)'>
        <div style='font-family:"Cormorant Garamond",serif;font-size:1.5rem;
        letter-spacing:0.08em;margin-bottom:0.5rem;color:var(--text)'>
            Lumi<em style='color:var(--gold)'>è</em>re
        </div>
        <div style='font-size:0.68rem;letter-spacing:0.25em;text-transform:uppercase;
        color:var(--text-muted)'>Luxury Fashion · Est. 2026</div>
    </div>
""", unsafe_allow_html=True)
