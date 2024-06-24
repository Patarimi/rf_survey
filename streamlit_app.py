import streamlit as st
import pandas as pd
import numpy as np
from menu import menu
import plotly.express as px


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
        sel_tech = list()
        popover = st.popover("Technology Filter")
        for sub_t in data["process"].unique():
            val = popover.checkbox(sub_t.split(".")[-1], value=True)
            if val:
                sel_tech.append(sub_t)
        col1.write("---")
        c1, c2 = st.columns([0.5, 0.5])
        data["ITRS FOM"] = (
            data["frequency"] ** 2 * data["sat_power"] * data["pae_max"] * data["gain"]
        )
        field_list = data.keys().drop(ignored_field).delete(0)
        x_name = c1.selectbox("X axis", field_list, index=1)
        y_name = c2.selectbox("Y axis", field_list, index=2)
        x_log = c1.checkbox("X Log scale", True)
        y_log = c2.checkbox("Y Log scale", False)
        colored = c1.checkbox("Colored", True)
        if colored:
            color_name = c1.selectbox(
                "Color", np.append(field_list.values, "process"), index=3
            )
        marker = c2.checkbox("Marker", False)
        if marker:
            marker_name = c2.selectbox("Marker", field_list, index=12)
    if col1.button("clear data"):
        load_data.clear()
    fig = px.scatter(
        data[data["process"].isin(sel_tech)],
        x=x_name,
        y=y_name,
        color=None if not colored else color_name,
        symbol=None if not (marker) else marker_name,
        hover_name="author_name",
        hover_data=["year"],
        log_x=x_log,
        log_y=y_log,
        labels={x_name: x_name, y_name: y_name},
    )
    event = col2.plotly_chart(fig, use_container_width=True, on_select="rerun")
    if event:
        st.write("## Selected Data:")
        st.write(
            data.drop(columns=["Unnamed: 0", "month"]).loc[
                data.index.isin(event.selection.point_indices)
            ]
        )
    col2.write(
        "**Source** : Hua Wang, Kyungsik Choi, Basem Abdelaziz, Mohamed Eleraky, Bryan Lin, Edward Liu, Yuqi Liu, "
        "Hossein Jalili, Mohsen Ghorbanpoor, Chenhao Chu, Tzu-Yuan Huang, Naga Sasikanth Mannem, Jeongsoo Park, "
        "Jeongseok Lee, David Munzer,Sensen Li, Fei Wang, Amr S. Ahmed, Christopher Snyder, Huy Thong Nguyen, "
        'and Michael Edward Duffy Smith, "*Power Amplifiers Performance Survey 2000-Present,*" '
        "[Online]. Available: https://ideas.ethz.ch/Surveys/pa-survey.html"
    )
