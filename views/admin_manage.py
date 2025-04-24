import streamlit as st  

if not st.session_state.get("admin"):
    st.warning("You do not have permission to view this page.")
    st.switch_page("views/user_content.py")

st.title("Employees Management")



