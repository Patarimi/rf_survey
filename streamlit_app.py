import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import matplotlib as mpl
import numpy as np
from scipy.spatial import ConvexHull

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df


# field to ignore for the data plot
ignored_field = {"paper_title", "author_name", "month"}

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
    col1, _, col2 = st.columns([0.3, 0.1, 0.6])
    with col1:
        st.title("Welcome!")
        comp = st.selectbox("Component Type", ("PA",))
        col1.write("---")
        techno = st.selectbox(
            "Technology", ["CMOS", "SiGe", "GaN", "GaAs", "InP", "LDMOS", "Others"]
        )
        data = load_data(f"data/cleaned/{techno}.csv")
        sel_tech = dict()
        popover = st.popover("Technology Filter")
        for sub_t in data["process"].unique():
            sel_tech[sub_t] = popover.checkbox(sub_t.split(".")[-1], value=True)
        col1.write("---")
        c1, c2 = st.columns([0.5, 0.5])
        field_list = data.keys().drop(ignored_field).delete(0)
        x_name = c1.selectbox("X axis", field_list, index=2)
        y_name = c2.selectbox("Y axis", field_list, index=3)
        x_log = c1.checkbox("X Log scale", True)
        x_min, x_max = np.min(data[x_name]), np.max(data[x_name])
        x_min_u, x_max_u = col1.slider("Rescale X", x_min, x_max, (x_min, x_max))
        y_log = c2.checkbox("Y Log scale", False)
    col1.write("---")
    if col1.button("clear data"):
        load_data.clear()
    fig, ax = plt.subplots()
    for i, process in enumerate(sel_tech):
        if not sel_tech[process]:
            continue
        subset = data.loc[
            (data["process"] == process)
            & (data[x_name] > x_min_u)
            & (data[x_name] < x_max_u)
            & (data[y_name] != np.NaN)
            , [x_name, y_name]].dropna()
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
        if subset.shape[0] > 3:
            hull = ConvexHull(subset)
            array = np.array(subset)
            for simplex in hull.simplices:
                ax.plot(array[simplex, 0], array[simplex, 1], color=cmap[i % 10], linestyle="--")
    ax.grid(True)
    col2.pyplot(fig, use_container_width=True)
    st.write(
        "**Source** : Hua Wang, Kyungsik Choi, Basem Abdelaziz, Mohamed Eleraky, Bryan Lin, Edward Liu, Yuqi Liu, "
        "Hossein Jalili, Mohsen Ghorbanpoor, Chenhao Chu, Tzu-Yuan Huang, Naga Sasikanth Mannem, Jeongsoo Park, "
        "Jeongseok Lee, David Munzer,Sensen Li, Fei Wang, Amr S. Ahmed, Christopher Snyder, Huy Thong Nguyen, "
        'and Michael Edward Duffy Smith, "*Power Amplifiers Performance Survey 2000-Present,*" '
        "[Online]. Available: https://ideas.ethz.ch/Surveys/pa-survey.html"
    )
