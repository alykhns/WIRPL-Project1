import streamlit as st
from components.style import inject_style
from components.navbar import render_navbar
from utils.api_client import login
from utils.session import init_session
from components.toast import show_success, show_error

st.set_page_config(page_title="Login - Lumière", page_icon="🔐", layout="wide")

init_session()
inject_style()
render_navbar()

# Page Header
st.markdown("""
    <div style='text-align:center;margin: 3rem 0 2rem'>
        <span style='font-size:0.68rem;letter-spacing:0.35em;text-transform:uppercase;color:var(--gold)'>Welcome Back</span>
        <h1 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:3rem;margin-top:0.5rem;color:var(--text)'>
            Login to <em style='color:var(--gold)'>Lumière</em>
        </h1>
        <div style='width:60px;height:1px;background:var(--gold);margin:1.5rem auto'></div>
    </div>
""", unsafe_allow_html=True)

# Login Form Container
col1, col2, col3 = st.columns([1, 1.5, 1])

with col2:
    with st.container(border=True):
        with st.form("login_form_page"):
            l_email = st.text_input("Email", placeholder="your@email.com")
            l_pass = st.text_input("Password", type="password", placeholder="••••••••")
            
            st.markdown("<div style='margin-top: 1.5rem'></div>", unsafe_allow_html=True)
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not l_email or not l_pass:
                    show_error("Email dan Password wajib diisi.")
                else:
                    data = login(l_email, l_pass)
                    if data and "token" in data:
                        st.session_state["token"] = data["token"]
                        st.session_state["user"] = data["name"]
                        show_success(f"Welcome back, {data['name']}!")
                        st.switch_page("Home.py")
                    else:
                        show_error("Login Gagal: Email atau Password salah.")

    st.markdown("""
        <div style='text-align:center;margin-top:1.5rem'>
            <p style='font-size:0.85rem;color:var(--text-muted)'>
                Don't have an account? 
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Create New Account", use_container_width=True):
        st.switch_page("pages/8_Register.py")

# Footer
st.markdown("<div style='margin-top:5rem'></div>", unsafe_allow_html=True)
