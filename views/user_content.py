import streamlit as st
import os
from streamlit_image_coordinates import streamlit_image_coordinates
from components.footer import display_footer


_, feed_col, _ = st.columns([1,5,1])

# Landing page with direct navigation
with feed_col.container(key="landing_container"):
    admin_col, client_col, employee_col = st.columns(3)

    # Container for Admin
    with admin_col.container(key="feed_container_1"):
        admin_click = streamlit_image_coordinates(
            source=r"static\images\admin.png", 
            key="admin", 
            use_column_width=True
        )
        if admin_click:
            # Check if admin is already logged in
            if st.session_state.get("admin"):
                st.switch_page("views/admin_dashboard.py")
            else:
                st.switch_page("views/admin_auth.py")

    # Container for Client
    with client_col.container(key="feed_container_2"):
        client_click = streamlit_image_coordinates(
            source=r"static\images\client.png", 
            key="client", 
            use_column_width=True
        )
        if client_click:
            st.switch_page("views/client_content.py")

    # Container for Employee
    with employee_col.container(key="feed_container_3"):
        employee_click = streamlit_image_coordinates(
            source=r"static\images\employee.png", 
            key="employee", 
            use_column_width=True
        )
        if employee_click:
            st.switch_page("views/employee_content.py")

    # Display footer
    display_footer()