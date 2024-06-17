import streamlit as st
from menu import menu


st.title("Login Page")
login = st.text_input("Login")
password = st.text_input("Password", type="password")

cred = st.secrets["admin_credentials"]
if st.button("Login"):
    if login == cred.username and password == cred.password:
        st.session_state.role = "admin"
        st.switch_page("streamlit_app.py")

menu()
