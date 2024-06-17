import streamlit as st


def authenticated_menu():
    st.sidebar.page_link("app.py", label="Main Page")
    st.sidebar.page_link("pages/edit_data.py", label="Edit Data")
    st.sidebar.page_link("pages/logout.py", label="Log Out")


def unauthenticated_menu():
    st.sidebar.page_link("app.py", label="Main Page")
    st.sidebar.page_link("pages/login.py", label="Log in")


def menu():
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
    else:
        authenticated_menu()


def menu_with_redirect():
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()
