import streamlit as st
import os
from streamlit_image_coordinates import streamlit_image_coordinates
from components.footer import display_footer

# Set root path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# This MUST be the first st.* call
st.set_page_config(
    page_title="Palayan Citizen Hub", 
    layout="wide", 
    initial_sidebar_state="collapsed", 
    page_icon=os.path.join(ROOT_PATH, "static", "images", "palayan-logo-png.png")
)

# Load custom CSS
with open(os.path.join(ROOT_PATH, "static", "css", "styles.css")) as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# Initialize session state for admin authentication
if "admin" not in st.session_state:
    st.session_state["admin"] = None

# Define all pages
user = st.Page("views/user_content.py", title="Welcome", default=True)
admin_auth = st.Page("views/admin_auth.py", title="Admin")
client = st.Page("views/client_content.py", title="Client")
employee = st.Page("views/employee_content.py", title="Employee")

# Admin pages
admin_dashboard = st.Page("views/admin_dashboard.py", title="Admin Dashboard")
admin_manage_users = st.Page("views/admin_manage.py", title="Employees Management")


pg = st.navigation([user, admin_auth, client, employee, admin_dashboard, admin_manage_users], position="hidden")

# Run the selected page
pg.run()