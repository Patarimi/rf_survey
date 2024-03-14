import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import matplotlib as mpl

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
    st.title("Welcome !")
    cmap = mpl.colormaps.get_cmap("tab10").colors
    data = pd.read_excel("data/PA-Survey-v8.xlsx", sheet_name="CMOS")
    col1, col2 = st.columns([0.3, 0.7])
    x_name = col1.selectbox('X axis', data.keys(), index=7)
    y_name = col1.selectbox('Y axis', data.keys(), index=8)
    x_log = col1.checkbox('X Log scale', True)
    y_log = col1.checkbox('Y Log scale', False)
    fig, ax = plt.subplots()
    for i, process in enumerate(data['Process'].unique()):
        subset = data.loc[data['Process'] == process]
        subset.plot(x=x_name,
                    y=y_name, kind="scatter",
                    ax=ax, logx=x_log, logy=y_log, label=process,
                    color=cmap[i % 10])
    col2.pyplot(fig)

    st.write(
        '**Source** : Hua Wang, Kyungsik Choi, Basem Abdelaziz, Mohamed Eleraky, Bryan Lin, Edward Liu, Yuqi Liu, '
        'Hossein Jalili, Mohsen Ghorbanpoor, Chenhao Chu, Tzu-​Yuan Huang, Naga Sasikanth Mannem, Jeongsoo Park, '
        'Jeongseok Lee, David Munzer,Sensen Li, Fei Wang, Amr S. Ahmed, Christopher Snyder, Huy Thong Nguyen, '
        'and Michael Edward Duffy Smith, "*Power Amplifiers Performance Survey 2000-​Present,*" '
        '[Online]. Available: https://ideas.ethz.ch/Surveys/pa-​survey.html'
    )
