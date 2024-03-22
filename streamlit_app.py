import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import matplotlib as mpl


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df


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
    cmap = mpl.colormaps.get_cmap("tab10").colors
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        st.title("Welcome!")
        st.write("Please select a technology.")
        techno = st.selectbox(
            "Technology", ["CMOS", "SiGe", "GaN", "GaAs", "InP", "LDMOS", "Others"]
        )
        data = load_data(f"data/cleaned/{techno}.csv")
        x_name = st.selectbox("X axis", data.keys(), index=6)
        y_name = st.selectbox("Y axis", data.keys(), index=7)
        x_log = st.checkbox("X Log scale", True)
        y_log = st.checkbox("Y Log scale", False)
    fig, ax = plt.subplots()
    for i, process in enumerate(data["process"].unique()):
        subset = data.loc[data["process"] == process]
        subset.plot(
            x=x_name,
            y=y_name,
            kind="scatter",
            ax=ax,
            logx=x_log,
            logy=y_log,
            label=process.split(".")[-1],
            color=cmap[i % 10],
        )
    col2.pyplot(fig)

    col1.write(
        "**Source** : Hua Wang, Kyungsik Choi, Basem Abdelaziz, Mohamed Eleraky, Bryan Lin, Edward Liu, Yuqi Liu, "
        "Hossein Jalili, Mohsen Ghorbanpoor, Chenhao Chu, Tzu-Yuan Huang, Naga Sasikanth Mannem, Jeongsoo Park, "
        "Jeongseok Lee, David Munzer,Sensen Li, Fei Wang, Amr S. Ahmed, Christopher Snyder, Huy Thong Nguyen, "
        'and Michael Edward Duffy Smith, "*Power Amplifiers Performance Survey 2000-Present,*" '
        "[Online]. Available: https://ideas.ethz.ch/Surveys/pa-survey.html"
    )
