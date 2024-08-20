import glob
from os.path import basename
import streamlit as st
from pages.menu import menu_with_redirect
import pandas as pd
from processing.data_preparation import PASpec

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("Data Edition Page")
tu = glob.glob("data/cleaned/*")
selected = st.selectbox("Please select files", [basename(file) for file in tu])
path = f"data/cleaned/{selected}"
df = pd.read_csv(path, usecols=PASpec.model_fields)
corrected = st.data_editor(df, key="data_editor", hide_index=True)
