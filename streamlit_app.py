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
            "Report a bug": "https://github.com/Patarimi/rf-survey/issues",
        },
    )
    st.title("Welcome")
    data = pd.read_excel("data/PA-Survey-v8.xlsx", sheet_name="CMOS")
    col1, col2 = st.columns([0.3, 0.7])
    col1.write(data.keys())
    fig, ax = plt.subplots()
    data.plot(x="Frequency (GHz)", y="Psat (dBm)", kind="scatter", ax=ax, logx=True)
    col2.pyplot(fig)

    st.write(
        'Source : Hua Wang, Kyungsik Choi, Basem Abdelaziz, Mohamed Eleraky, Bryan Lin, Edward Liu, Yuqi Liu, Hossein Jalili, Mohsen Ghorbanpoor, Chenhao Chu, Tzu-​Yuan Huang, Naga Sasikanth Mannem, Jeongsoo Park, Jeongseok Lee, David Munzer,Sensen Li, Fei Wang, Amr S. Ahmed, Christopher Snyder, Huy Thong Nguyen, and Michael Edward Duffy Smith, "Power Amplifiers Performance Survey 2000-​Present," [Online]. Available: https://ideas.ethz.ch/Surveys/pa-​survey.html'
    )
