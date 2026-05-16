# frontend/pages/5_Riwayat.py

import streamlit as st
from utils.session import init_session
from utils.api_client import get_order_history, get_profile, update_profile
from utils.formatter import format_price, get_status_color, get_status_bg
from components.style import inject_style
from components.toast import show_success

inject_style()
init_session()

st.markdown("""
    <div style='padding:2rem 0 1rem'>
        <span style='font-size:0.68rem;letter-spacing:0.35em;
        text-transform:uppercase;color:#C9A96E'>account</span>
        <h1 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:2.5rem'>
            My <em style='color:#C9A96E'>Profile</em>
        </h1>
        <div style='width:40px;height:1px;background:#C9A96E;margin-top:0.8rem'></div>
    </div>
""", unsafe_allow_html=True)

col_sidebar, col_content = st.columns([1, 3])

with col_sidebar:
    profile = get_profile()
    full_name = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()
    initial = full_name[0] if full_name else "A"

    st.markdown(f"""
        <div style='width:80px;height:80px;border-radius:50%;
        background:linear-gradient(135deg,#C9A96E,#8B6914);
        display:flex;align-items:center;justify-content:center;
        font-family:"Cormorant Garamond",serif;font-size:2rem;
        color:white;font-style:italic;margin-bottom:1rem'>
            {initial}
        </div>
        <div style='font-family:"Cormorant Garamond",serif;font-size:1.3rem'>
            {profile.get("name", "")}
        </div>
        <div style='font-size:0.75rem;color:#8A8476;margin-bottom:0.5rem'>
            {profile.get("email", "")}
        </div>
        <div style='display:inline-block;background:#C9A96E;color:white;
        font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;
        padding:3px 10px;margin-bottom:1.5rem'>
            {profile.get("membership", "member")}
        </div>
    """, unsafe_allow_html=True)

    tab = st.radio(
        "menu",
        ["order history", "personal info", "security"],
        label_visibility="collapsed",
    )

with col_content:
    if "order history" in tab:
        st.markdown("<h3 style='font-family:\"Cormorant Garamond\",serif;font-weight:300;margin-bottom:1.5rem'>Order <em style=\"color:#C9A96E\">History</em></h3>", unsafe_allow_html=True)

        orders = get_order_history()
        #st.write(orders[0]) 
        for order in orders:
            parts = []
            for i in order["items"]:
                parts.append(i["product_name"] + " x" + str(i["qty"]))
            item_names = ", ".join(parts)
            status = order.get("status", "")
            total = order["total"]
            st.markdown(f"""
                <div style='display:flex;justify-content:space-between;align-items:center;
                padding:1rem;border:1px solid rgba(201,169,110,0.25);margin-bottom:0.8rem'>
                    <div>
                        <div style='font-size:0.85rem;font-weight:500'>{order["order_id"]}</div>
                        <div style='font-size:0.75rem;color:#8A8476'>{order["date"]}</div>
                        <div style='font-size:0.78rem;color:#1A1A1A;margin-top:0.3rem'>
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
                        <div style='font-size:0.9rem;font-weight:500'>
                            {format_price(total)}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    elif "personal info" in tab:
        st.markdown("<h3 style='font-family:\"Cormorant Garamond\",serif;font-weight:300;margin-bottom:1.5rem'>Personal <em style=\"color:#C9A96E\">Info</em></h3>", unsafe_allow_html=True)

        with st.form("profile_form"):
            c1, c2 = st.columns(2)
            name = c1.text_input("full name", value=profile.get("name", ""))
            phone = c2.text_input("phone", value=profile.get("phone", ""))
            email = st.text_input("email", value=profile.get("email", ""), disabled=True)

            if st.form_submit_button("save changes", use_container_width=True):
                update_profile({"name": name, "phone": phone})
                show_success("profile updated")

    elif "security" in tab:
        st.markdown("<h3 style='font-family:\"Cormorant Garamond\",serif;font-weight:300;margin-bottom:1.5rem'>Security <em style=\"color:#C9A96E\">Settings</em></h3>", unsafe_allow_html=True)

        with st.form("password_form"):
            current = st.text_input("current password", type="password")
            new_pass = st.text_input("new password", type="password")
            confirm = st.text_input("confirm new password", type="password")

            if st.form_submit_button("update password", use_container_width=True):
                if new_pass == confirm and len(new_pass) >= 6:
                    show_success("password updated")
                else:
                    st.error("passwords don't match or too short")