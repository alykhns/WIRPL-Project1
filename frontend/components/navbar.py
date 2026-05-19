import streamlit as st
from utils.session import is_logged_in, logout, init_session
from utils.api_client import get_cart, get_profile
from components.style import inject_style


def render_navbar():
    """
    Render the main navigation bar at the top of the page.
    Uses st.page_link for persistent session and single-window navigation.
    """
    init_session()
    inject_style()
    
    # Navbar Container at the top
    nav_container = st.container()
    
    with nav_container:
        # Layout: Logo | Links... | Cart | Profile/Login
        cols = st.columns([2, 1, 1, 1, 1, 1, 1.5, 1.5])
        
        with cols[0]:
            st.markdown('<div style="font-family: \'Cormorant Garamond\', serif; font-size: 1.5rem; font-weight: 400; letter-spacing: 0.08em; color: var(--text);">Lumi<em style="color: var(--gold); font-style: italic;">è</em>re</div>', unsafe_allow_html=True)
        
        with cols[1]:
            st.page_link("Home.py", label="Home")
        
        with cols[2]:
            st.page_link("pages/1_Katalog.py", label="Katalog")
            
        with cols[3]:
            st.page_link("pages/5_Riwayat.py", label="Riwayat")
            
        # Admin link only if logged in and admin
        with cols[4]:
            if is_logged_in():
                user = get_profile()
                membership_level = user.get('membership_level', 'regular').lower()
                IS_ADMIN = membership_level in ['platinum', 'admin'] or user.get('email') == "admin@lumiere.com"
                if IS_ADMIN:
                    st.page_link("pages/6_Admin.py", label="Admin")
        
        # Spacer
        with cols[5]:
            st.write("")
            
        with cols[6]:
            cart_items = get_cart()
            cart_count = len(cart_items) if cart_items else 0
            st.page_link("pages/3_Cart.py", label=f"◇ Cart ({cart_count})")
            
        with cols[7]:
            if is_logged_in():
                user = get_profile()
                name = user.get('first_name', 'User')
                if st.button(f"👤 {name} (Logout)", key="nav_logout", use_container_width=True):
                    logout()
                    st.rerun()
            else:
                if st.button("🔐 Login", key="nav_login", use_container_width=True):
                    st.switch_page("Home.py")

    st.markdown('<hr style="margin-top: 0.5rem; margin-bottom: 2rem; border: 0; border-top: 1px solid var(--hr);">', unsafe_allow_html=True)


def navbar_cart_badge():
    """
    Display cart badge in navbar area (for reference).
    """
    cart_count = st.session_state.get("cart_count", 0)
    if cart_count > 0:
        return f"◇ Cart ({cart_count})"
    return "◇ Cart"


def render_mobile_navbar():
    """
    Render a mobile-friendly navbar.
    """
    init_session()
    
    st.markdown("""
        <style>
        .mobile-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--bg);
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-around;
            padding: 0.5rem 0;
            z-index: 9998;
        }
        .mobile-nav-item {
            flex: 1;
            text-align: center;
            font-size: 0.8rem;
            color: var(--text-muted);
        }
        </style>
    """, unsafe_allow_html=True)


def breadcrumb(items: list):
    """
    Display breadcrumb navigation.
    """
    breadcrumb_html = '<div style="margin-bottom: 1.5rem;">'
    for idx, item in enumerate(items):
        if isinstance(item, tuple):
            label, path = item
            breadcrumb_html += f'<a href="{path}" style="color: var(--gold); text-decoration: none; font-size: 0.85rem;">{label}</a>'
        else:
            breadcrumb_html += f'<span style="color: var(--text-muted); font-size: 0.85rem;">{item}</span>'
        if idx < len(items) - 1:
            breadcrumb_html += ' <span style="color: var(--gold); margin: 0 0.5rem;">›</span> '
    breadcrumb_html += '</div>'
    st.markdown(breadcrumb_html, unsafe_allow_html=True)


def navbar_search():
    """
    Render a search component for the navbar.
    """
    st.markdown("""
        <style>
        .navbar-search {
            display: flex;
            gap: 0.5rem;
            align-items: center;
            margin: 1rem 0;
        }
        .navbar-search input {
            flex: 1;
            padding: 0.5rem;
            border: 1px solid var(--border);
            border-radius: 4px;
            font-size: 0.85rem;
            background-color: var(--card-bg);
            color: var(--text);
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input(
            "Search products...",
            placeholder="Search by name, brand...",
            label_visibility="collapsed",
            key="navbar_search"
        )
    with col2:
        st.button("🔍", help="Search")
    
    return search_query
