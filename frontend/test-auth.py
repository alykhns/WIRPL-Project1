import streamlit as st
import requests

# Konfigurasi Backend
BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Auth API Tester", page_icon="🔐")

st.title("🔐 Auth API Tester")
st.info("Gunakan halaman ini untuk memverifikasi integrasi FastAPI + Supabase.")

# --- SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "token" not in st.session_state:
    st.session_state["token"] = None
if "user_name" not in st.session_state:
    st.session_state["user_name"] = None

# --- STATUS LOGIN ---
st.subheader("📊 Current Status")
if st.session_state["logged_in"]:
    st.success(f"✅ STATUS: LOGGED IN")
    st.write(f"**Nama:** {st.session_state['user_name']}")
    st.write(f"**Token:** `{st.session_state['token'][:20]}...` (Terpotong)")
    if st.button("Log Out"):
        # Panggil API Logout (Opsional)
        requests.post(f"{BASE_URL}/logout")
        # Bersihkan Session
        for key in ["logged_in", "token", "user_name"]:
            st.session_state[key] = None
        st.session_state["logged_in"] = False
        st.rerun()
else:
    st.error("❌ STATUS: NOT LOGGED IN")

st.divider()

# --- INTERFACE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Register")
    with st.form("reg_form"):
        r_email = st.text_input("Email")
        r_pass = st.text_input("Password", type="password")
        r_first = st.text_input("First Name")
        r_last = st.text_input("Last Name")
        r_phone = st.text_input("Phone Number")
        if st.form_submit_button("Register"):
            payload = {
                "email": r_email,
                "password": r_pass,
                "first_name": r_first,
                "last_name": r_last,
                "phone_number": r_phone
            }
            res = requests.post(f"{BASE_URL}/register", json=payload)
            if res.ok:
                st.success("Registrasi Berhasil! Silakan Login.")
            else:
                st.error(f"Error: {res.json().get('detail')}")

with col2:
    st.subheader("🔑 Login")
    with st.form("login_form"):
        l_email = st.text_input("Email")
        l_pass = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            payload = {"email": l_email, "password": l_pass}
            res = requests.post(f"{BASE_URL}/login", json=payload)
            if res.ok:
                data = res.json()
                st.session_state["logged_in"] = True
                st.session_state["token"] = data["token"]
                st.session_state["user_name"] = data["name"]
                st.success("Login Berhasil!")
                st.rerun()
            else:
                st.error("Login Gagal: Email atau Password salah.")

st.divider()
st.caption("Pastikan Backend (FastAPI) berjalan di http://localhost:8000")
