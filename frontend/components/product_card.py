import streamlit as st
from utils.formatter import format_price
from utils.api_client import add_to_cart
from components.toast import show_success, show_error


def product_card(product, show_add_to_cart=True):
    """
    Display a product card with product details and add to cart button.
    """
    
    with st.container(border=True):
        col1, col2 = st.columns([2, 3])
        
        with col1:
            image_url = product.get("image_url")
            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                image_initial = product.get("name", "P")[0].upper()
                st.markdown(f"""
                    <div style="
                        width: 100%;
                        aspect-ratio: 1;
                        background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%);
                        border-radius: 8px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 3rem;
                        color: white;
                        font-family: 'Cormorant Garamond', serif;
                        font-weight: 600;
                    ">
                        {image_initial}
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <p style="margin: 0; font-size: 0.9rem; color: var(--text-muted); letter-spacing: 0.08em;">
                    {product.get('brand', 'Brand').upper()}
                </p>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <h3 style="margin: 4px 0 8px 0; font-size: 1.3rem; font-family: 'Cormorant Garamond', serif; color: var(--text); font-weight: 400;">
                    {product.get('name', 'Product')}
                </h3>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <p style="margin: 0; font-size: 1.4rem; color: var(--gold); font-weight: 600;">
                    {format_price(product.get('price', 0))}
                </p>
            """, unsafe_allow_html=True)
            
            # Handle both 'stock' (real DB) and 'inventory_count' (mock data)
            inventory = product.get("stock")
            if inventory is None:
                inventory = product.get("inventory_count", 0)
                
            status_color = "#27AE60" if inventory > 0 else "#C0392B"
            status_text = f"In Stock ({inventory})" if inventory > 0 else "Out of Stock"
            
            st.markdown(f"""
                <p style="margin: 8px 0; font-size: 0.75rem; color: {status_color}; font-weight: 500; letter-spacing: 0.05em;">
                    {status_text}
                </p>
            """, unsafe_allow_html=True)
            
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
                    <p style="margin: 0; font-size: 0.75rem; color: var(--text-muted); line-height: 1.6;">
                        {' • '.join(attributes)}
                    </p>
                """, unsafe_allow_html=True)
            
            description = product.get("description")
            if description:
                st.caption(description[:100] + "..." if len(description) > 100 else description)
        
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
                        result = add_to_cart(product_id=product.get("product_id"), quantity=1)
                        if result:
                            show_success(f"✓ {product.get('name', 'Product')} added to cart!")
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
                    st.session_state["selected_product_id"] = product.get("product_id")
                    st.switch_page("pages/2_Detail_Produk.py")


def product_grid(products, columns=3, show_add_to_cart=True):
    cols = st.columns(columns)
    for idx, product in enumerate(products):
        with cols[idx % columns]:
            product_card(product, show_add_to_cart=show_add_to_cart)
