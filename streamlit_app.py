import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import matplotlib as mpl
import numpy as np


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df


if __name__ == "__main__":
    st.set_page_config(
        page_title="RF-survey",
        page_icon="📈",
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
        comp = st.selectbox("Component Type", ("PA",))
        techno = st.selectbox(
            "Technology", ["CMOS", "SiGe", "GaN", "GaAs", "InP", "LDMOS", "Others"]
        )
        data = load_data(f"data/cleaned/{techno}.csv")
        col1.write("---")
        sel_tech = dict()
        for sub_t in data["process"].unique():
            sel_tech[sub_t] = st.checkbox(sub_t, value=True)
        c1, c2 = st.columns([0.5, 0.5])
        x_name = c1.selectbox("X axis", data.keys(), index=6)
        y_name = c2.selectbox("Y axis", data.keys(), index=7)
        x_log = c1.checkbox("X Log scale", True)
        x_min = np.min(data[x_name])
        x_max = np.max(data[x_name])
        x_min_u, x_max_u = c1.slider("Rescale", x_min, x_max, (x_min, x_max))
        y_log = c2.checkbox("Y Log scale", False)
    fig, ax = plt.subplots()
    for i, process in enumerate(sel_tech):
        if not sel_tech[process]:
            continue
        subset = data.loc[
            (data["process"] == process)
            & (data[x_name] > x_min_u)
            & (data[x_name] < x_max_u)
        ]
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
    ax.grid(True)
    col2.pyplot(fig, use_container_width=True)
    col1.write("---")
    col1.write(
        "**Source** : Hua Wang, Kyungsik Choi, Basem Abdelaziz, Mohamed Eleraky, Bryan Lin, Edward Liu, Yuqi Liu, "
        "Hossein Jalili, Mohsen Ghorbanpoor, Chenhao Chu, Tzu-Yuan Huang, Naga Sasikanth Mannem, Jeongsoo Park, "
        "Jeongseok Lee, David Munzer,Sensen Li, Fei Wang, Amr S. Ahmed, Christopher Snyder, Huy Thong Nguyen, "
        'and Michael Edward Duffy Smith, "*Power Amplifiers Performance Survey 2000-Present,*" '
        "[Online]. Available: https://ideas.ethz.ch/Surveys/pa-survey.html"
    )
    if st.button("clear data"):
        load_data.clear()
