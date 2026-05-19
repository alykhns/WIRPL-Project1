import streamlit as st
from utils.formatter import format_price
from utils.api_client import add_to_cart
from components.toast import show_success, show_error


def product_card(product, show_add_to_cart=True):
    """
    Display a product card with product details and add to cart button.
    
    Args:
        product (dict): Product data containing:
            - product_id, product_name, brand, price, color, size
            - material, style, season, inventory_count, category_id
            - arrival_date, description, image_url (optional)
        show_add_to_cart (bool): Whether to show the add to cart button
    """
    
    with st.container(border=True):
        # Product Image Placeholder
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # Product image - use image_url if available, otherwise show initial
            image_url = product.get("image_url")
            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                image_initial = product.get("product_name", "P")[0].upper()
                st.markdown(f"""
                    <div style="
                        width: 100%;
                        aspect-ratio: 1;
                        background: linear-gradient(135deg, #C9A96E 0%, #E8D5B0 100%);
                        border-radius: 8px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 3rem;
                        color: rgba(250, 247, 242, 0.8);
                        font-family: 'Cormorant Garamond', serif;
                        font-weight: 600;
                    ">
                        {image_initial}
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Product Details
            st.markdown(f"""
                <p style="margin: 0; font-size: 0.9rem; color: #8A8476; letter-spacing: 0.08em;">
                    {product.get('brand', 'Brand').upper()}
                </p>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <h3 style="margin: 4px 0 8px 0; font-size: 1.3rem; font-family: 'Cormorant Garamond', serif; color: #1A1A1A; font-weight: 400;">
                    {product.get('product_name', 'Product')}
                </h3>
            """, unsafe_allow_html=True)
            
            # Price
            st.markdown(f"""
                <p style="margin: 0; font-size: 1.4rem; color: #C9A96E; font-weight: 600;">
                    {format_price(product.get('price', 0))}
                </p>
            """, unsafe_allow_html=True)
            
            # Inventory status
            inventory = product.get("inventory_count", 0)
            status_color = "#27AE60" if inventory > 0 else "#C0392B"
            status_text = "In Stock" if inventory > 0 else "Out of Stock"
            
            st.markdown(f"""
                <p style="margin: 8px 0; font-size: 0.75rem; color: {status_color}; font-weight: 500; letter-spacing: 0.05em;">
                    {status_text}
                </p>
            """, unsafe_allow_html=True)
            
            # Attributes
            attributes = []
            if product.get("color"):
                attributes.append(f"<strong>Color:</strong> {product['color']}")
            if product.get("size"):
                attributes.append(f"<strong>Size:</strong> {product['size']}")
            if product.get("material"):
                attributes.append(f"<strong>Material:</strong> {product['material']}")
            if product.get("style"):
                attributes.append(f"<strong>Style:</strong> {product['style']}")
            if product.get("season"):
                attributes.append(f"<strong>Season:</strong> {product['season']}")
            
            if attributes:
                st.markdown(f"""
                    <p style="margin: 0; font-size: 0.75rem; color: #8A8476; line-height: 1.6;">
                        {' • '.join(attributes)}
                    </p>
                """, unsafe_allow_html=True)
            
            # Description
            description = product.get("description")
            if description:
                st.caption(description[:100] + "..." if len(description) > 100 else description)
            
            # Arrival date
            arrival_date = product.get("arrival_date")
            if arrival_date:
                st.caption(f"📅 Arrived: {arrival_date}")
        
        # Add to Cart Button
        if show_add_to_cart:
            st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button(
                    "🛒 Add to Cart",
                    key=f"add_cart_{product.get('product_id', 'unknown')}",
                    use_container_width=True,
                ):
                    if inventory > 0:
                        result = add_to_cart(
                            product_id=product.get("product_id"),
                            quantity=1
                        )
                        if result:
                            show_success(f"✓ {product.get('product_name', 'Product')} added to cart!")
                        else:
                            show_error("✗ Failed to add product to cart")
                    else:
                        show_error("✗ Product out of stock")
            
            with col_btn2:
                if st.button(
                    "👁 View Details",
                    key=f"detail_{product.get('product_id', 'unknown')}",
                    use_container_width=True,
                ):
                    # Navigate to detail page
                    st.session_state["selected_product"] = product
                    st.switch_page("pages/2_Detail_Produk.py")


def product_grid(products, columns=3, show_add_to_cart=True):
    """
    Display products in a grid layout.
    
    Args:
        products (list): List of product dictionaries
        columns (int): Number of columns in the grid
        show_add_to_cart (bool): Whether to show add to cart buttons
    """
    cols = st.columns(columns)
    
    for idx, product in enumerate(products):
        with cols[idx % columns]:
            product_card(product, show_add_to_cart=show_add_to_cart)
