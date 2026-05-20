import streamlit as st
from components.style import inject_style
from components.navbar import render_navbar
from utils.api_client import register
from utils.session import init_session
from components.toast import show_success, show_error

st.set_page_config(page_title="Register - Lumière", page_icon="✨", layout="wide")

init_session()
inject_style()
render_navbar()

# Page Header
st.markdown("""
    <div style='text-align:center;margin: 3rem 0 2rem'>
        <span style='font-size:0.68rem;letter-spacing:0.35em;text-transform:uppercase;color:var(--gold)'>Join the Circle</span>
        <h1 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:3rem;margin-top:0.5rem;color:var(--text)'>
            Create <em style='color:var(--gold)'>Account</em>
        </h1>
        <div style='width:60px;height:1px;background:var(--gold);margin:1.5rem auto'></div>
    </div>
""", unsafe_allow_html=True)

# Register Form Container
col1, col2, col3 = st.columns([1, 1.8, 1])

with col2:
    with st.container(border=True):
        with st.form("reg_form_page"):
            r_email = st.text_input("Email", placeholder="your@email.com")
            r_pass = st.text_input("Password", type="password", placeholder="Minimum 6 characters")
            
            c1, c2 = st.columns(2)
            with c1:
                r_first = st.text_input("First Name", placeholder="John")
            with c2:
                r_last = st.text_input("Last Name", placeholder="Doe")
            
            r_phone = st.text_input("Phone Number", placeholder="+62...")
            
            st.markdown("<div style='margin-top: 1.5rem'></div>", unsafe_allow_html=True)
            submit = st.form_submit_button("Create Account", use_container_width=True)
            
            if submit:
                if not r_email or not r_pass or not r_first:
                    show_error("Mohon lengkapi data yang wajib diisi.")
                else:
                    res = register(r_email, r_pass, r_first, r_last, r_phone)
                    if res:
                        show_success("Registrasi Berhasil! Silakan Login.")
                        st.switch_page("pages/7_Login.py")
                    else:
                        show_error("Registrasi Gagal. Silakan coba lagi.")

    st.markdown("""
        <div style='text-align:center;margin-top:1.5rem'>
            <p style='font-size:0.85rem;color:var(--text-muted)'>
                Already have an account? 
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Back to Login", use_container_width=True):
        st.switch_page("pages/7_Login.py")

# Footer
st.markdown("<div style='margin-top:5rem'></div>", unsafe_allow_html=True)
