import streamlit as st
import os
import pandas as pd
import random
import plotly.express as px

# Assuming AdminService is a valid class and doesn't need mocking for this example
# from services.admin_service import AdminService

# # Check if user is authenticated as admin
# if not st.session_state.get("admin"):
# # st.switch_page("views/admin_auth.py")
#     pass # Commented out for mock data example

# Initialize services
# admin_service = AdminService()

# --- Service Initialization (Cached) ---
# @st.cache_resource
# def get_admin_service() -> AdminService:
#     return AdminService()

# Add logout button in the top right
logout_col = st.container()
with logout_col:
    # if st.button("Logout", key="logout_button"):
    #     # Clear admin from session state
    #     st.session_state["admin"] = None
    #     if not st.session_state.get("admin"):
    #         st.switch_page("views/user_content.py")
    pass # Commented out for mock data example


with st.container(key="employee_container"):

    emp_metric_col, client_metric_col, rating_metric_col, processed_queues_metric_col = st.columns(4)

    # Mock Data for Metrics
    num_employees = 150
    num_clients = 500
    processed_queues_this_week = 1200
    avg_rating = 4.5

    # Number of Employees
    emp_metric_col.metric(label="No. of Employees", value=num_employees, border=True)
    # Number of Clients
    client_metric_col.metric(label="No. of Clients", value=num_clients, border=True)
    # Number of Processed Queues this week (mon to sunday)
    processed_queues_metric_col.metric(label="Processed Queues this week", value=processed_queues_this_week, border=True)
    # Average Rating for all Employees
    rating_metric_col.metric(label="Emp Avg Rating", value=avg_rating, border=True)


    weekly_queue_count_col, emp_rating_distribution_col, top_rated_employees_col = st.columns(3)

    # Mock Data for Charts
    # Weekly Queue Count
    week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    queue_counts = [random.randint(100, 300) for _ in range(7)]
    weekly_queue_df = pd.DataFrame({'Day': week_days, 'Queue Count': queue_counts})

    # Employee Rating Distribution
    ratings = [random.randint(1, 5) for _ in range(num_employees)]
    rating_distribution = pd.DataFrame({'Rating': ratings})
    rating_distribution = rating_distribution['Rating'].value_counts().reset_index()
    rating_distribution.columns = ['Rating', 'Count']
    rating_distribution = rating_distribution.sort_values('Rating')


    # Top Rated Employees
    employee_names = [f'Employee {i}' for i in range(1, num_employees + 1)]
    employee_ratings = [round(random.uniform(4.0, 5.0), 2) for _ in range(num_employees)]
    employee_df = pd.DataFrame({'Employee Name': employee_names, 'Rating': employee_ratings})
    top_employees = employee_df.sort_values('Rating', ascending=False).head(10)


    # Weekly Queue Count (plotly bar chart)
    with weekly_queue_count_col:
        st.subheader("Weekly Queue Count")
        fig_weekly_queue = px.bar(weekly_queue_df, x='Day', y='Queue Count', title='Weekly Queue Count')
        st.plotly_chart(fig_weekly_queue, use_container_width=True)

    # Employee Rating Distribution (plotly horizontal bar chart)
    with emp_rating_distribution_col:
        st.subheader("Employee Rating Distribution")
        fig_rating_distribution = px.bar(rating_distribution, x='Count', y='Rating', orientation='h', title='Employee Rating Distribution')
        st.plotly_chart(fig_rating_distribution, use_container_width=True)

    # Top Rated Employees (plotly horizontal bar chart)
    with top_rated_employees_col:
        st.subheader("Top 10 Employees by Rating")
        fig_top_employees = px.bar(top_employees.sort_values('Rating'), x='Rating', y='Employee Name', orientation='h', title='Top 10 Employees by Rating')
        st.plotly_chart(fig_top_employees, use_container_width=True)