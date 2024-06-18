import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Spectral6
from bokeh.models import HoverTool
import numpy as np
from scipy.spatial import ConvexHull
from menu import menu


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df


def set_role():
    # Callback function to save the role selection to Session State
    st.session_state.role = st.session_state._role


# field to ignore for the data plot
ignored_field = {"paper_title", "author_name", "month", "process", "modulation_type"}

if __name__ == "__main__":
    if "role" not in st.session_state:
        st.session_state.role = None
    st.session_state._role = st.session_state.role
    st.set_page_config(
        page_title="RF-survey",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Report a bug": "https://github.com/Patarimi/rf-survey/issues",
        },
    )
    menu()
    col1, col2 = st.columns([0.25, 0.75])
    with col1:
        st.title("Welcome!")
        comp = st.selectbox("Component Type", ("PA",))
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
        data["ITRS FOM"] = (
            data["frequency"] ** 2 * data["sat_power"] * data["pae_max"] * data["gain"]
        )
        field_list = data.keys().drop(ignored_field).delete(0)
        x_name = c1.selectbox("X axis", field_list, index=1)
        y_name = c2.selectbox("Y axis", field_list, index=2)
        x_log = c1.checkbox("X Log scale", True)
        x_min, x_max = np.min(data[x_name]), np.max(data[x_name])
        x_min_u, x_max_u = col1.slider("Rescale X", x_min, x_max, (x_min, x_max))
        y_log = c2.checkbox("Y Log scale", False)
        draw_hull = col1.checkbox("SoA contour", True)
    if col1.button("clear data"):
        load_data.clear()
    tooltips = "@author_name:@year"
    p = figure(
        title=f"State of Art of PA in {techno}",
        x_axis_label=x_name,
        y_axis_label=y_name,
        x_axis_type="log" if x_log else "linear",
        y_axis_type="log" if y_log else "linear",
    )
    hvr = HoverTool(tooltips=tooltips)
    p.add_tools(hvr)
    sca = list()
    for i, process in enumerate(sel_tech):
        if not sel_tech[process]:
            continue
        subset = data.loc[
            (data["process"] == process)
            & (data[x_name] >= x_min_u)
            & (data[x_name] <= x_max_u),
            [x_name, y_name, "year", "author_name"],
        ].dropna()
        sca.append(
            p.scatter(
                x=x_name,
                y=y_name,
                source=subset,
                marker="o",
                color=Spectral6[i % 6],
                legend_label=process.split(".")[-1],
            )
        )
        hull_set = subset.loc[(data["process"] == process), [x_name, y_name]]
        if x_log:
            hull_set[x_name] = np.log10(hull_set[x_name])
        if y_log:
            hull_set[y_name] = np.log10(hull_set[y_name])
        if not draw_hull:
            continue
        if hull_set.shape[0] > 3:
            array = np.array(hull_set.dropna())
            hull = ConvexHull(array)
            x, y = list(), list()
            for simplex in hull.vertices:
                x.append(10 ** array[simplex, 0] if x_log else array[simplex, 0])
                y.append(10 ** array[simplex, 1] if y_log else array[simplex, 1])
            p.patch(x, y, color=Spectral6[i % 6], fill_alpha=0.1, line_alpha=1)
        else:
            p.patch(
                hull_set[x_name],
                hull_set[y_name],
                color=Spectral6[i % 6],
                fill_alpha=0.1,
                line_alpha=1,
            )
    hvr.renderers = sca
    col2.bokeh_chart(p, use_container_width=True)
    col2.write(
        "**Source** : Hua Wang, Kyungsik Choi, Basem Abdelaziz, Mohamed Eleraky, Bryan Lin, Edward Liu, Yuqi Liu, "
        "Hossein Jalili, Mohsen Ghorbanpoor, Chenhao Chu, Tzu-Yuan Huang, Naga Sasikanth Mannem, Jeongsoo Park, "
        "Jeongseok Lee, David Munzer,Sensen Li, Fei Wang, Amr S. Ahmed, Christopher Snyder, Huy Thong Nguyen, "
        'and Michael Edward Duffy Smith, "*Power Amplifiers Performance Survey 2000-Present,*" '
        "[Online]. Available: https://ideas.ethz.ch/Surveys/pa-survey.html"
    )
