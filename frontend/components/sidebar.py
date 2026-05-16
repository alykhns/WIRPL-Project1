import streamlit as st
from utils.session import is_logged_in, logout, init_session
from utils.api_client import get_profile, get_cart
from utils.formatter import format_price
from utils.mock_data import MOCK_CATEGORIES


def render_sidebar():
    """
    Render the main sidebar with user info, filters, and navigation.
    Filters are based on product table fields from database:
    - category_id (from categories table join)
    - price (decimal from product table)
    - size, material, style, season (varchar fields from product table)
    """
    init_session()
    
    with st.sidebar:
        # User Section
        st.markdown("---")
        render_user_section()
        
        st.markdown("---")
        st.subheader("🔍 FILTERS", divider="gold")
        
        # Category Filter
        render_category_filter()
        
        # Price Range Filter
        render_price_filter()
        
        # Size Filter
        render_size_filter()
        
        # Material Filter
        render_material_filter()
        
        # Style Filter
        render_style_filter()
        
        # Season Filter
        render_season_filter()
        
        # Apply/Clear Filters
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Apply", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("✕ Clear", use_container_width=True):
                clear_all_filters()
                st.rerun()


def render_user_section():
    """
    Render user profile section in sidebar.
    """
    if is_logged_in():
        user = get_profile()
        cart_count = len(get_cart()) if get_cart() else 0
        
        # User Info
        first_name = user.get('first_name', 'User')
        last_name = user.get('last_name', '')
        st.write(f"### 👤 {first_name} {last_name}")
        st.caption(user.get('email', 'user@example.com'))
        
        # Membership Level Badge
        membership = user.get('membership_level', 'regular').capitalize()
        membership_colors = {
            "Platinum": "#C9A96E",
            "Gold": "#FFD700",
            "Silver": "#C0C0C0",
            "Regular": "#8A8476",
        }
        color = membership_colors.get(membership, "#8A8476")
        st.markdown(f"""
            <p style="
                display: inline-block;
                background-color: {color}20;
                color: {color};
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 600;
                letter-spacing: 0.05em;
            ">
                ◆ {membership.upper()}
            </p>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Actions
        col_profile, col_cart = st.columns(2)
        
        with col_profile:
            if st.button("📝 Profile", use_container_width=True):
                st.info("Redirect to profile page")
        
        with col_cart:
            if st.button(f"🛒 Cart ({cart_count})", use_container_width=True):
                st.switch_page("pages/3_Cart.py")
        
        # Logout Button
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
    
    else:
        st.write("### 👤 Welcome Guest")
        st.caption("Sign in to your account")
        
        col_login, col_register = st.columns(2)
        
        with col_login:
            if st.button("🔐 Login", use_container_width=True):
                st.info("Redirect to login page")
        
        with col_register:
            if st.button("📝 Register", use_container_width=True):
                st.info("Redirect to register page")


def render_category_filter():
    """
    Render category filter section based on database categories.
    Categories from: categories table (category_id, category_name)
    """
    st.write("**Category**")
    
    # Get categories from mock data (in production, fetch from database)
    categories = list(MOCK_CATEGORIES.values())
    selected_categories = st.multiselect(
        "Select categories",
        options=categories,
        default=st.session_state.get("filter_categories", []),
        label_visibility="collapsed",
        key="filter_categories_select"
    )
    
    st.session_state["filter_categories"] = selected_categories


def render_price_filter():
    """
    Render price range filter section.
    Price from product table: decimal(10,2) in IDR
    """
    st.write("**Price Range**")
    
    min_price = st.session_state.get("filter_min_price", 0)
    max_price = st.session_state.get("filter_max_price", 1000000)
    
    price_range = st.slider(
        "Select price range (Rp)",
        min_value=0,
        max_value=1000000,
        value=(min_price, max_price),
        step=10000,
        label_visibility="collapsed",
        key="filter_price_range"
    )
    
    st.session_state["filter_min_price"] = price_range[0]
    st.session_state["filter_max_price"] = price_range[1]
    
    # Display formatted price range
    st.caption(f"Rp {price_range[0]:,.0f} - Rp {price_range[1]:,.0f}".replace(",", "."))


def render_size_filter():
    """
    Render size filter section.
    Size from product table: varchar(50)
    """
    st.write("**Size**")
    
    # Common sizes for clothing
    sizes = ["XS", "S", "M", "L", "XL", "XXL"]
    selected_sizes = st.multiselect(
        "Select sizes",
        options=sizes,
        default=st.session_state.get("filter_sizes", []),
        label_visibility="collapsed",
        key="filter_sizes_select"
    )
    
    st.session_state["filter_sizes"] = selected_sizes


def render_material_filter():
    """
    Render material filter section.
    Material from product table: varchar(100)
    """
    st.write("**Material**")
    
    materials = ["cotton", "silk", "polyester", "linen", "wool", "denim"]
    selected_materials = st.multiselect(
        "Select materials",
        options=materials,
        default=st.session_state.get("filter_materials", []),
        label_visibility="collapsed",
        key="filter_materials_select"
    )
    
    st.session_state["filter_materials"] = selected_materials


def render_style_filter():
    """
    Render style filter section.
    Style from product table: varchar(100)
    """
    st.write("**Style**")
    
    styles = ["casual", "formal", "sporty", "vintage", "bohemian", "minimalist", "eveningwear"]
    selected_styles = st.multiselect(
        "Select styles",
        options=styles,
        default=st.session_state.get("filter_styles", []),
        label_visibility="collapsed",
        key="filter_styles_select"
    )
    
    st.session_state["filter_styles"] = selected_styles


def render_season_filter():
    """
    Render season filter section.
    Season from product table: varchar(50)
    """
    st.write("**Season**")
    
    seasons = ["spring", "summer", "fall", "winter"]
    selected_seasons = st.multiselect(
        "Select seasons",
        options=seasons,
        default=st.session_state.get("filter_seasons", []),
        label_visibility="collapsed",
        key="filter_seasons_select"
    )
    
    st.session_state["filter_seasons"] = selected_seasons


def clear_all_filters():
    """
    Clear all active filters and reset to default values.
    """
    st.session_state["filter_categories"] = []
    st.session_state["filter_sizes"] = []
    st.session_state["filter_materials"] = []
    st.session_state["filter_styles"] = []
    st.session_state["filter_seasons"] = []
    st.session_state["filter_min_price"] = 0
    st.session_state["filter_max_price"] = 1000000
    st.toast("✓ All filters cleared!")


def get_active_filters():
    """
    Get all active filters as a dictionary.
    Returns filter values matching product table fields.
    
    Returns:
        dict: Dictionary containing all active filter values
    """
    return {
        "categories": st.session_state.get("filter_categories", []),
        "min_price": st.session_state.get("filter_min_price", 0),
        "max_price": st.session_state.get("filter_max_price", 1000000),
        "sizes": st.session_state.get("filter_sizes", []),
        "materials": st.session_state.get("filter_materials", []),
        "styles": st.session_state.get("filter_styles", []),
        "seasons": st.session_state.get("filter_seasons", []),
    }


def filter_products(products, filters=None):
    """
    Filter products based on active filters.
    Products must have fields from product table: 
    product_id, category_id, price, size, material, style, season
    
    Args:
        products (list): List of product dictionaries from database
        filters (dict): Optional custom filters dictionary
    
    Returns:
        list: Filtered list of products matching all criteria
    """
    if filters is None:
        filters = get_active_filters()
    
    filtered = products
    
    # Filter by category (using category_id from product table)
    if filters.get("categories"):
        category_ids = [
            cat_id for cat_id, cat_name in MOCK_CATEGORIES.items()
            if cat_name in filters["categories"]
        ]
        filtered = [p for p in filtered if p.get("category_id") in category_ids]
    
    # Filter by price range
    min_price = filters.get("min_price", 0)
    max_price = filters.get("max_price", 1000000)
    filtered = [
        p for p in filtered
        if min_price <= p.get("price", 0) <= max_price
    ]
    
    # Filter by size
    if filters.get("sizes"):
        filtered = [p for p in filtered if p.get("size") in filters["sizes"]]
    
    # Filter by material
    if filters.get("materials"):
        filtered = [p for p in filtered if p.get("material") in filters["materials"]]
    
    # Filter by style
    if filters.get("styles"):
        filtered = [p for p in filtered if p.get("style") in filters["styles"]]
    
    # Filter by season
    if filters.get("seasons"):
        filtered = [p for p in filtered if p.get("season") in filters["seasons"]]
    
    return filtered


def render_filter_summary():
    """
    Display a summary of active filters above the product list.
    """
    filters = get_active_filters()
    
    active_count = sum([
        len(filters.get("categories", [])),
        len(filters.get("sizes", [])),
        len(filters.get("materials", [])),
        len(filters.get("styles", [])),
        len(filters.get("seasons", [])),
        1 if filters.get("min_price", 0) > 0 or filters.get("max_price", 1000000) < 1000000 else 0,
    ])
    
    if active_count > 0:
        st.info(f"🔍 {active_count} filter(s) active")
        
        # Show active filters as chips
        col_filters = st.columns(4)
        col_idx = 0
        
        for category in filters.get("categories", []):
            with col_filters[col_idx % 4]:
                st.caption(f"📁 {category}")
                col_idx += 1
        
        for size in filters.get("sizes", []):
            with col_filters[col_idx % 4]:
                st.caption(f"📏 {size}")
                col_idx += 1
        
        for material in filters.get("materials", []):
            with col_filters[col_idx % 4]:
                st.caption(f"🧵 {material}")
                col_idx += 1
        
        for style in filters.get("styles", []):
            with col_filters[col_idx % 4]:
                st.caption(f"✨ {style}")
                col_idx += 1
        
        for season in filters.get("seasons", []):
            with col_filters[col_idx % 4]:
                st.caption(f"🌤️ {season}")
                col_idx += 1


def render_compact_sidebar():
    """
    Render a compact version of sidebar for pages that need minimal space.
    """
    with st.sidebar:
        st.markdown("---")
        
        if is_logged_in():
            user = get_profile()
            first_name = user.get('first_name', 'Profile')
            if st.button(f"👤 {first_name}", use_container_width=True):
                st.info("Profile page")
            
            if st.button("🚪 Logout", use_container_width=True):
                logout()
                st.rerun()
        
        else:
            if st.button("🔐 Login", use_container_width=True):
                st.info("Login page")
