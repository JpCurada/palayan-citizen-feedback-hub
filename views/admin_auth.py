import streamlit as st

from components.footer import display_footer
from services.admin_service import AdminService


# --- Service Initialization (Cached) ---
@st.cache_resource
def get_admin_service() -> AdminService:
    return AdminService()

# Check if already authenticated - if so, redirect to dashboard
if st.session_state.get("admin"):
    st.switch_page("views/admin_dashboard.py")

def check_admin_access(email: str, access_code: str) -> bool:
    admin_service = get_admin_service()
    admin = admin_service.get_admin_by_email(email)
    if admin and access_code == st.secrets["ACCESS_CODE"]:
        return admin, True
    return None, False


_, feed_col, _ = st.columns([1, 2, 1])
with feed_col.container(key="form_container_1"):
    st.subheader("Welcome, Admin")
    st.markdown("Please fill out the form below to get **access to the admin dashboard**.")

    # Registration form as a fragment
    @st.fragment
    def login_form():
        email = st.text_input("Email", placeholder="Enter your email")
        access_code = st.text_input("Access Code", type="password", placeholder="Enter the Access Code")
        
        login_col, end_col = st.columns([2,1])

        with login_col:
            submit_button = st.button(
                label="Login", 
                disabled=True if not email or not access_code else False,
                use_container_width=True
            )

        with end_col:
            back_button = st.button(
                label="Back",
                use_container_width=True
            )
        
        if submit_button:
            # Handle auth logic here
            admin, is_authenticated = check_admin_access(email, access_code)
            
            if admin and is_authenticated:
                # Store admin in session state for persistence
                st.session_state["admin"] = admin
                st.switch_page("views/admin_dashboard.py")
            else:
                st.toast("Double check your Email and Access code")
            
        if back_button:
            st.switch_page("views/user_content.py")

    login_form()
