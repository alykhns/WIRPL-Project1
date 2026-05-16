import streamlit as st

def init_session():
    defaults = {
        "token": None,
        "user": None,
        "cart_count": 0,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def is_logged_in():
    return st.session_state.get("token") is not None

def logout():
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.cart_count = 0