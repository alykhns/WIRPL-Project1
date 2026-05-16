import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

from utils.session import is_logged_in, logout, init_session
from utils.api_client import get_profile, get_order_history, get_cart
from utils.formatter import format_price, get_status_color, get_status_bg
from utils.mock_data import (
    MOCK_USER, MOCK_ORDERS, MOCK_PRODUCTS_SAMPLE, 
    MOCK_CATEGORIES, MOCK_CART
)
from components.style import inject_style
from components.navbar import render_navbar


# Page config
st.set_page_config(
    page_title="Admin - Lumière",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize
init_session()
inject_style()
render_navbar()

# Check admin access
user = get_profile()
membership_level = user.get('membership_level', '').lower()

if not is_logged_in() or membership_level not in ['platinum', 'admin']:
    st.error("❌ Access Denied: Admin Panel is for authorized users only")
    st.info("Please log in with an admin account")
    st.stop()

# Admin Dashboard Header
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

# Admin Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard",
    "📦 Products",
    "📁 Categories",
    "📋 Orders",
    "👥 Customers",
    "📈 Reports"
])


# ==================== TAB 1: DASHBOARD ====================
with tab1:
    st.subheader("Dashboard Overview")
    
    # Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = len(MOCK_ORDERS)
        st.metric("Total Orders", total_orders, "+5 this week")
    
    with col2:
        total_revenue = sum([order["total"] for order in MOCK_ORDERS])
        st.metric("Total Revenue", format_price(total_revenue), "+12.5%")
    
    with col3:
        total_products = len(MOCK_PRODUCTS_SAMPLE)
        st.metric("Total Products", total_products, "+2 new")
    
    with col4:
        total_categories = len(MOCK_CATEGORIES)
        st.metric("Categories", total_categories, "Active")
    
    st.markdown("---")
    
    # Order Status Distribution
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Order Status Distribution")
        status_counts = {}
        for order in MOCK_ORDERS:
            status = order.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        if status_counts:
            st.bar_chart(pd.DataFrame({
                "Status": list(status_counts.keys()),
                "Count": list(status_counts.values())
            }).set_index("Status"))
    
    with col_right:
        st.subheader("Recent Orders")
        recent_orders = sorted(MOCK_ORDERS, key=lambda x: x["date"], reverse=True)[:5]
        
        for order in recent_orders:
            status_color = get_status_color(order["status"])
            status_bg = get_status_bg(order["status"])
            
            st.markdown(f"""
                <div style="
                    padding: 1rem;
                    border-radius: 8px;
                    border-left: 4px solid {status_color};
                    background: {status_bg};
                    margin-bottom: 0.5rem;
                ">
                    <p style="margin: 0; font-weight: 600; color: #1A1A1A;">
                        {order['order_id']} - {format_price(order['total'])}
                    </p>
                    <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; color: {status_color};">
                        {order['status'].upper()} • {order['date']}
                    </p>
                </div>
            """, unsafe_allow_html=True)


# ==================== TAB 2: PRODUCTS ====================
with tab2:
    st.subheader("Product Management")
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("➕ Add New Product", use_container_width=True):
            st.session_state.show_add_product = True
    with col_btn2:
        search_product = st.text_input("Search products...", placeholder="Search by name, brand, or ID")
    
    st.markdown("---")
    
    # Show add product form if needed
    if st.session_state.get("show_add_product", False):
        st.info("📝 Add New Product Form")
        
        with st.form("add_product_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                product_name = st.text_input("Product Name")
                brand = st.text_input("Brand")
                price = st.number_input("Price (Rp)", min_value=0, value=100000)
                category_id = st.selectbox("Category", options=list(MOCK_CATEGORIES.keys()), format_func=lambda x: MOCK_CATEGORIES[x])
            
            with col2:
                color = st.text_input("Color")
                size = st.selectbox("Size", ["XS", "S", "M", "L", "XL", "XXL"])
                material = st.text_input("Material")
                style = st.text_input("Style")
            
            description = st.text_area("Description")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                season = st.selectbox("Season", ["spring", "summer", "fall", "winter"])
            with col_b:
                inventory = st.number_input("Inventory Count", min_value=0, value=100)
            with col_c:
                arrival_date = st.date_input("Arrival Date")
            
            col_submit, col_cancel = st.columns(2)
            with col_submit:
                if st.form_submit_button("✓ Add Product", use_container_width=True):
                    st.success("✓ Product added successfully!")
                    st.session_state.show_add_product = False
            
            with col_cancel:
                if st.form_submit_button("✕ Cancel", use_container_width=True):
                    st.session_state.show_add_product = False
    
    # Products Table
    st.subheader("Product List")
    
    products_display = MOCK_PRODUCTS_SAMPLE
    if search_product:
        products_display = [
            p for p in products_display
            if search_product.lower() in p.get("product_name", "").lower()
            or search_product.lower() in p.get("brand", "").lower()
        ]
    
    # Create products dataframe
    products_df = pd.DataFrame([
        {
            "ID": p.get("product_id"),
            "Name": p.get("product_name"),
            "Brand": p.get("brand"),
            "Category": MOCK_CATEGORIES.get(p.get("category_id"), "Unknown"),
            "Price": format_price(p.get("price", 0)),
            "Stock": p.get("inventory_count"),
            "Status": "✓ In Stock" if p.get("inventory_count", 0) > 0 else "✗ Out of Stock"
        }
        for p in products_display
    ])
    
    st.dataframe(products_df, use_container_width=True, hide_index=True)


# ==================== TAB 3: CATEGORIES ====================
with tab3:
    st.subheader("Category Management")
    
    if st.button("➕ Add New Category", use_container_width=False):
        st.session_state.show_add_category = True
    
    st.markdown("---")
    
    # Show add category form
    if st.session_state.get("show_add_category", False):
        st.info("📝 Add New Category")
        
        with st.form("add_category_form"):
            category_name = st.text_input("Category Name")
            category_desc = st.text_area("Description (optional)")
            
            col_submit, col_cancel = st.columns(2)
            with col_submit:
                if st.form_submit_button("✓ Add Category", use_container_width=True):
                    st.success("✓ Category added successfully!")
                    st.session_state.show_add_category = False
            with col_cancel:
                if st.form_submit_button("✕ Cancel", use_container_width=True):
                    st.session_state.show_add_category = False
    
    # Categories Table
    st.subheader("Category List")
    
    categories_df = pd.DataFrame([
        {
            "ID": cat_id,
            "Name": cat_name,
            "Products": len([p for p in MOCK_PRODUCTS_SAMPLE if p.get("category_id") == cat_id]),
            "Status": "Active"
        }
        for cat_id, cat_name in MOCK_CATEGORIES.items()
    ])
    
    st.dataframe(categories_df, use_container_width=True, hide_index=True)


# ==================== TAB 4: ORDERS ====================
with tab4:
    st.subheader("Order Management")
    
    # Filter options
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        status_filter = st.multiselect(
            "Filter by Status",
            options=["delivered", "shipping", "processing", "cancelled"],
            default=["delivered", "shipping", "processing"]
        )
    
    with col_filter2:
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            format="YYYY-MM-DD"
        )
    
    with col_filter3:
        sort_by = st.selectbox("Sort by", ["Latest", "Oldest", "Highest Value", "Lowest Value"])
    
    st.markdown("---")
    
    # Orders Table
    st.subheader("Order List")
    
    orders_display = MOCK_ORDERS
    if status_filter:
        orders_display = [o for o in orders_display if o["status"] in status_filter]
    
    # Sort
    if sort_by == "Latest":
        orders_display = sorted(orders_display, key=lambda x: x["date"], reverse=True)
    elif sort_by == "Oldest":
        orders_display = sorted(orders_display, key=lambda x: x["date"])
    elif sort_by == "Highest Value":
        orders_display = sorted(orders_display, key=lambda x: x["total"], reverse=True)
    else:
        orders_display = sorted(orders_display, key=lambda x: x["total"])
    
    # Create orders dataframe
    orders_df = pd.DataFrame([
        {
            "Order ID": o.get("order_id"),
            "Date": o.get("date"),
            "Total": format_price(o.get("total", 0)),
            "Items": len(o.get("items", [])),
            "Status": o.get("status", "unknown").upper()
        }
        for o in orders_display
    ])
    
    st.dataframe(orders_df, use_container_width=True, hide_index=True)
    
    # Detailed view
    st.subheader("Order Details")
    selected_order_id = st.selectbox(
        "Select Order",
        options=[o["order_id"] for o in orders_display],
        format_func=lambda x: f"{x} - Details"
    )
    
    selected_order = next((o for o in MOCK_ORDERS if o["order_id"] == selected_order_id), None)
    
    if selected_order:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Order ID", selected_order["order_id"])
        with col2:
            st.metric("Date", selected_order["date"])
        with col3:
            st.metric("Status", selected_order["status"].upper())
        
        st.markdown("---")
        st.write("**Items:**")
        
        items_data = []
        for item in selected_order.get("items", []):
            items_data.append({
                "Product": item.get("product_name"),
                "Brand": item.get("brand"),
                "Qty": item.get("qty"),
                "Price": format_price(item.get("price_at_purchase", 0)),
                "Subtotal": format_price(item.get("qty", 0) * item.get("price_at_purchase", 0))
            })
        
        if items_data:
            items_df = pd.DataFrame(items_data)
            st.dataframe(items_df, use_container_width=True, hide_index=True)
        
        st.write(f"**Total: {format_price(selected_order['total'])}**")
        
        # Update status
        new_status = st.selectbox(
            "Update Order Status",
            options=["delivered", "shipping", "processing", "cancelled"],
            index=["delivered", "shipping", "processing", "cancelled"].index(selected_order["status"])
        )
        
        if st.button("✓ Update Status", use_container_width=False):
            st.success(f"✓ Order status updated to {new_status.upper()}")


# ==================== TAB 5: CUSTOMERS ====================
with tab5:
    st.subheader("Customer Management")
    
    search_customer = st.text_input("Search customers by name or email...")
    
    st.markdown("---")
    
    # Customer statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Customers", 1000, "↑ 50 new")
    with col2:
        st.metric("Active Users", 856, "85.6%")
    with col3:
        st.metric("Platinum Members", 42, "4.2%")
    
    st.markdown("---")
    
    # Customer List (mock)
    st.subheader("Customer List")
    
    customers_data = [
        {
            "Customer ID": 1,
            "Name": f"{MOCK_USER['first_name']} {MOCK_USER['last_name']}",
            "Email": MOCK_USER["email"],
            "Phone": MOCK_USER["phone_number"],
            "Membership": MOCK_USER["membership_level"].upper(),
            "Orders": len(MOCK_ORDERS),
            "Total Spent": format_price(sum([o["total"] for o in MOCK_ORDERS]))
        }
    ]
    
    customers_df = pd.DataFrame(customers_data)
    st.dataframe(customers_df, use_container_width=True, hide_index=True)
    
    # Customer Details
    st.subheader("Customer Profile")
    
    with st.form("customer_details"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("First Name", value=MOCK_USER["first_name"], disabled=True)
            st.text_input("Email", value=MOCK_USER["email"], disabled=True)
            st.text_input("Gender", value=MOCK_USER["gender"], disabled=True)
        
        with col2:
            st.text_input("Last Name", value=MOCK_USER["last_name"], disabled=True)
            st.text_input("Phone", value=MOCK_USER["phone_number"], disabled=True)
            st.text_input("Membership", value=MOCK_USER["membership_level"].upper(), disabled=True)
        
        st.text_input("Address", value=MOCK_USER["address"], disabled=True)
        st.text_input("City", value=MOCK_USER["city"], disabled=True)
        
        if st.form_submit_button("Edit Customer"):
            st.info("Edit functionality coming soon")


# ==================== TAB 6: REPORTS ====================
with tab6:
    st.subheader("Sales Reports")
    
    # Report Type Selection
    report_type = st.selectbox(
        "Select Report Type",
        options=[
            "Sales Summary",
            "Product Performance",
            "Customer Segmentation",
            "Inventory Status",
            "Revenue Trend"
        ]
    )
    
    st.markdown("---")
    
    if report_type == "Sales Summary":
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Total Sales**")
            total_sales = sum([o["total"] for o in MOCK_ORDERS])
            st.metric("This Month", format_price(total_sales))
        
        with col2:
            st.write("**Average Order Value**")
            avg_order = total_sales / len(MOCK_ORDERS) if MOCK_ORDERS else 0
            st.metric("AOV", format_price(avg_order))
        
        st.markdown("---")
        st.write("**Sales by Status**")
        
        status_summary = {}
        for order in MOCK_ORDERS:
            status = order["status"]
            status_summary[status] = status_summary.get(status, 0) + order["total"]
        
        summary_df = pd.DataFrame({
            "Status": list(status_summary.keys()),
            "Revenue": [format_price(v) for v in status_summary.values()],
            "Amount (Raw)": list(status_summary.values())
        })
        
        st.bar_chart(summary_df.set_index("Status")["Amount (Raw)"])
    
    elif report_type == "Product Performance":
        st.write("**Top Products by Sales**")
        
        product_sales = {}
        for order in MOCK_ORDERS:
            for item in order.get("items", []):
                product_name = item.get("product_name")
                amount = item.get("qty", 0) * item.get("price_at_purchase", 0)
                product_sales[product_name] = product_sales.get(product_name, 0) + amount
        
        if product_sales:
            perf_df = pd.DataFrame({
                "Product": list(product_sales.keys()),
                "Sales": [format_price(v) for v in product_sales.values()],
                "Amount (Raw)": list(product_sales.values())
            })
            
            st.dataframe(perf_df, use_container_width=True, hide_index=True)
    
    elif report_type == "Inventory Status":
        st.write("**Current Inventory Levels**")
        
        inventory_df = pd.DataFrame([
            {
                "Product": p.get("product_name"),
                "Stock": p.get("inventory_count"),
                "Status": "✓ Good" if p.get("inventory_count", 0) > 50 else "⚠️ Low" if p.get("inventory_count", 0) > 10 else "✗ Critical"
            }
            for p in MOCK_PRODUCTS_SAMPLE
        ])
        
        st.dataframe(inventory_df, use_container_width=True, hide_index=True)
    
    elif report_type == "Revenue Trend":
        st.write("**Revenue Over Time**")
        
        revenue_by_status = {}
        for order in MOCK_ORDERS:
            status = order["status"]
            revenue_by_status[status] = revenue_by_status.get(status, 0) + order["total"]
        
        trend_df = pd.DataFrame({
            "Status": list(revenue_by_status.keys()),
            "Revenue": list(revenue_by_status.values())
        })
        
        st.bar_chart(trend_df.set_index("Status"))
    
    # Export report
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download Report (CSV)"):
            st.success("✓ Report downloaded")
    
    with col2:
        if st.button("🖨️ Print Report"):
            st.info("Print functionality available in your browser")
    
    with col3:
        if st.button("📧 Email Report"):
            st.success("✓ Report sent to admin email")


# Footer with logout
st.markdown("---")
col_info, col_logout = st.columns([3, 1])

with col_info:
    st.caption(f"👤 Logged in as: {user.get('first_name', 'Admin')} ({user.get('membership_level', 'admin').upper()})")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with col_logout:
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()
