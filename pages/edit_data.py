import streamlit as st
from pages.menu import menu_with_redirect
import pandas as pd

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("Data Edition Page")
st.markdown(f"You are currently logged with the role of {st.session_state.role}.")

path = "data/cleaned/CMOS.csv"
df = pd.read_csv(path)
st.data_editor(df, key="data_editor")
