import streamlit as st

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