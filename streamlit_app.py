import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

if __name__ == "__main__":
    st.set_page_config(
        page_title="Passive Auto Design demo",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://passiveautodesign.netlify.app/",
            "Report a bug": "https://github.com/Patarimi/PassiveAutoDesign/issues",
        },
    )
    st.title("Welcome")
    data = pd.read_excel("data/PA-Survey-v8.xlsx", sheet_name="CMOS")
    col1, col2 = st.columns(2)
    col1.write(data.keys())
    fig, ax = plt.subplots()
    data.plot(x="Frequency (GHz)", y="Psat (dBm)", kind="scatter", ax=ax, logx=True)
    col2.pyplot(fig)
