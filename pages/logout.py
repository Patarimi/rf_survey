import streamlit as st
from menu import menu


st.title("Logout")
st.session_state.role = None
menu()
