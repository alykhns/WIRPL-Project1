import streamlit as st

def show_toast(message, icon="✦"):
    st.toast(f"{icon} {message}")

def show_success(message):
    show_toast(message, icon="✓")

def show_error(message):
    show_toast(message, icon="✗")