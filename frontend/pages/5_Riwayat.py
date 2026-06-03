# frontend/pages/5_Riwayat.py

import streamlit as st
from utils.session import init_session
from utils.api_client import get_order_history, get_profile, update_profile
from utils.formatter import format_price, get_status_color, get_status_bg
from components.style import inject_style
from components.navbar import render_navbar
from components.toast import show_success

init_session()
inject_style()
render_navbar()

st.markdown("""
    <div style='padding:2rem 0 1rem'>
        <span style='font-size:0.68rem;letter-spacing:0.35em;
        text-transform:uppercase;color:var(--gold)'>account</span>
        <h1 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:2.5rem;color:var(--text)'>
            My <em style='color:var(--gold)'>Profile</em>
        </h1>
        <div style='width:40px;height:1px;background:var(--gold);margin-top:0.8rem'></div>
    </div>
""", unsafe_allow_html=True)

col_sidebar, col_content = st.columns([1, 3])

with col_sidebar:
    profile = get_profile()
    full_name = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()
    initial = full_name[0] if full_name else "A"

    st.markdown(f"""
        <div style='width:80px;height:80px;border-radius:50%;
        background:linear-gradient(135deg,var(--gold),var(--gold-dark));
        display:flex;align-items:center;justify-content:center;
        font-family:"Cormorant Garamond",serif;font-size:2rem;
        color:white;font-style:italic;margin-bottom:1rem'>
            {initial}
        </div>
        <div style='font-family:"Cormorant Garamond",serif;font-size:1.3rem;color:var(--text)'>
            {profile.get("first_name", "")} {profile.get("last_name", "")}
        </div>
        <div style='font-size:0.75rem;color:var(--text-muted);margin-bottom:0.5rem'>
            {profile.get("email", "")}
        </div>
        <div style='display:inline-block;background:var(--gold);color:white;
        font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;
        padding:3px 10px;margin-bottom:1.5rem'>
            {profile.get("membership_level", "member")}
        </div>
    """, unsafe_allow_html=True)

    tab = st.radio(
        "menu",
        ["order history", "personal info"],
        label_visibility="collapsed",
    )

with col_content:
    if "order history" in tab:
        st.markdown("<h3 style='font-family:\"Cormorant Garamond\",serif;font-weight:300;margin-bottom:1.5rem;color:var(--text)'>Order <em style=\"color:var(--gold)\">History</em></h3>", unsafe_allow_html=True)

        orders = get_order_history()
        for order in orders:
            parts = []
            for i in order.get("items", []):
                parts.append(i.get("product_name", "Product") + " x" + str(i.get("qty", 1)))
            item_names = ", ".join(parts)
            status = order.get("status", "pending")
            total = order.get("total", 0)
            st.markdown(f"""
                <div style='display:flex;justify-content:space-between;align-items:center;
                padding:1rem;border:1px solid var(--border);background:var(--card-bg);margin-bottom:0.8rem'>
                    <div>
                        <div style='font-size:0.85rem;font-weight:500;color:var(--text)'>{order.get("order_id", "#")}</div>
                        <div style='font-size:0.75rem;color:var(--text-muted)'>{order.get("date", "2026")}</div>
                        <div style='font-size:0.78rem;color:var(--text);margin-top:0.3rem'>
                            {item_names}
                        </div>
                    </div>
                    <div style='text-align:right'>
                        <div style='display:inline-block;padding:3px 10px;font-size:0.65rem;
                        letter-spacing:0.1em;text-transform:uppercase;
                        background:{get_status_bg(status)};color:{get_status_color(status)};
                        margin-bottom:0.5rem'>
                            {status}
                        </div>
                        <div style='font-size:0.9rem;font-weight:500;color:var(--text)'>
                            {format_price(total)}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    elif "personal info" in tab:
        st.markdown("<h3 style='font-family:\"Cormorant Garamond\",serif;font-weight:300;margin-bottom:1.5rem;color:var(--text)'>Personal <em style=\"color:var(--gold)\">Info</em></h3>", unsafe_allow_html=True)

        with st.form("profile_form"):
            c1, c2 = st.columns(2)
            first_name = c1.text_input("first name", value=profile.get("first_name", ""))
            last_name = c2.text_input("last name", value=profile.get("last_name", ""))
            phone = st.text_input("phone", value=profile.get("phone_number", ""))
            email = st.text_input("email", value=profile.get("email", ""), disabled=True)

            if st.form_submit_button("save changes", use_container_width=True):
                update_profile({"first_name": first_name, "last_name": last_name, "phone_number": phone})
                show_success("profile updated")
                st.rerun()

