import streamlit as st
from menu import menu


st.title("Login Page")
login = st.text_input("Login")
password = st.text_input("Password", type="password")

try:
    cred = st.secrets["admin_credentials"]
except FileNotFoundError:
    print("Misconfigured Server, please see [secrets](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)")
if st.button("Login"):
    if login == cred.username and password == cred.password:
        st.session_state.role = "admin"
        st.switch_page("streamlit_app.py")

menu()
