import streamlit as st
from utils.session import is_logged_in, logout, init_session
from utils.api_client import get_cart, get_profile
from components.style import inject_style


def render_navbar():
    """
    Render the main navigation bar with logo, links, cart, and profile.
    """
    # Initialize session
    init_session()
    
    # Inject custom styles (including navbar styles)
    inject_style()
    
    # Get cart count
    cart_items = get_cart()
    cart_count = len(cart_items) if cart_items else 0
    
    # Update session cart count
    st.session_state["cart_count"] = cart_count
    
    # Navbar HTML/CSS is already rendered via inject_style()
    # This function adds interactive elements
    
    # Add navbar actions in sidebar (hidden but functional)
    with st.sidebar:
        st.markdown("---")
        
        if is_logged_in():
            # User is logged in - show profile and logout
            user = get_profile()
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                first_name = user.get('first_name', 'User')
                last_name = user.get('last_name', '')
                st.write(f"👤 {first_name} {last_name}")
                st.caption(user.get('email', ''))
            
            with col2:
                if st.button("🚪", help="Logout", key="logout_btn"):
                    logout()
                    st.rerun()
            
            st.markdown("---")
            st.write("📋 **Menu**")
            
            col_menu1, col_menu2 = st.columns(2)
            with col_menu1:
                if st.button("🏠 Home", use_container_width=True):
                    st.switch_page("pages/0_Home.py")
            with col_menu2:
                if st.button(f"🛒 Cart ({cart_count})", use_container_width=True):
                    st.switch_page("pages/3_Cart.py")
            
            col_menu3, col_menu4 = st.columns(2)
            with col_menu3:
                if st.button("📦 Katalog", use_container_width=True):
                    st.switch_page("pages/1_Katalog.py")
            with col_menu4:
                if st.button("📜 Riwayat", use_container_width=True):
                    st.switch_page("pages/5_Riwayat.py")
            
            membership_level = user.get('membership_level', '').lower()
            if membership_level in ['platinum', 'admin']:
                st.markdown("---")
                if st.button("⚙️ Admin Panel", use_container_width=True):
                    st.switch_page("pages/6_Admin.py")
        
        else:
            # User not logged in - show login/register options
            st.write("👤 **Not Logged In**")
            
            col_auth1, col_auth2 = st.columns(2)
            with col_auth1:
                if st.button("🔐 Login", use_container_width=True):
                    # Navigate to login page if exists, or show login modal
                    st.info("Redirect to login page")
            with col_auth2:
                if st.button("📝 Register", use_container_width=True):
                    # Navigate to register page if exists
                    st.info("Redirect to register page")
            
            st.markdown("---")
            st.write("📋 **Browse**")
            
            col_browse1, col_browse2 = st.columns(2)
            with col_browse1:
                if st.button("🏠 Home", use_container_width=True):
                    st.switch_page("pages/0_Home.py")
            with col_browse2:
                if st.button("📦 Katalog", use_container_width=True):
                    st.switch_page("pages/1_Katalog.py")


def navbar_cart_badge():
    """
    Display cart badge in navbar area (for reference).
    This is rendered via inject_style() but we keep this for clarity.
    """
    cart_count = st.session_state.get("cart_count", 0)
    if cart_count > 0:
        return f"◇ Cart ({cart_count})"
    return "◇ Cart"


def render_mobile_navbar():
    """
    Render a mobile-friendly navbar (alternative compact version).
    """
    init_session()
    
    st.markdown("""
        <style>
        .mobile-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(250, 247, 242, 0.96);
            border-top: 1px solid rgba(201, 169, 110, 0.25);
            display: flex;
            justify-content: space-around;
            padding: 0.5rem 0;
            z-index: 9998;
        }
        .mobile-nav-item {
            flex: 1;
            text-align: center;
            font-size: 0.8rem;
            color: #8A8476;
        }
        </style>
    """, unsafe_allow_html=True)


def breadcrumb(items: list):
    """
    Display breadcrumb navigation.
    
    Args:
        items (list): List of tuples (label, page_path) or just labels for current page
                     Example: [("Home", "/"), ("Katalog", "/Katalog"), ("Detail")]
    """
    breadcrumb_html = '<div style="margin-bottom: 1.5rem;">'
    
    for idx, item in enumerate(items):
        if isinstance(item, tuple):
            label, path = item
            breadcrumb_html += f'<a href="{path}" style="color: #C9A96E; text-decoration: none; font-size: 0.85rem;">{label}</a>'
        else:
            breadcrumb_html += f'<span style="color: #8A8476; font-size: 0.85rem;">{item}</span>'
        
        if idx < len(items) - 1:
            breadcrumb_html += ' <span style="color: #C9A96E; margin: 0 0.5rem;">›</span> '
    
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
            border: 1px solid rgba(201, 169, 110, 0.25);
            border-radius: 4px;
            font-size: 0.85rem;
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
