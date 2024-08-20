import streamlit as st
from pages.menu import menu


st.title("Logout")
st.session_state.role = None
menu()
