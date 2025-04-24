import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Tuple
from uuid import UUID

# Assuming these services and visualization module exist and work correctly
# Ensure the paths are correct based on your project structure
from services.employee_service import EmployeeService
from services.rating_service import RatingService
import utils.data.visualize as viz # Assumes viz module contains create_bar_chart and create_word_cloud

from components.footer import display_footer

# --- Service Initialization (Cached) ---
# Use st.cache_resource if services are resource-intensive to initialize
@st.cache_resource
def get_employee_service() -> EmployeeService:
    """Caches the EmployeeService instance."""
    return EmployeeService()

@st.cache_resource
def get_rating_service() -> RatingService:
    """Caches the RatingService instance."""
    return RatingService()

employee_service = get_employee_service()
rating_service = get_rating_service()


# --- Data Fetching and Preparation (Cached) ---
# Cache data that doesn't change during the session
@st.cache_data
def fetch_and_prepare_employee_data() -> Tuple[List[Any], Dict[UUID, Any], Dict[str, UUID], List[Dict[str, Any]], Dict[UUID, Dict[str, Any]]]:
    """
    Fetches all employees, calculates all employees' average ratings,
    and prepares data structures for efficient lookup and ranking.
    """
    employees = employee_service.get_all_employees()
    employee_dict = {emp.emp_id: emp for emp in employees}
    employee_name_to_id = {f"{emp.first_name} {emp.last_name}, {emp.position}": emp.emp_id for emp in employees}

    # Calculate average rating for each employee using the existing method
    all_avg_ratings_list = []
    for emp in employees:
        avg_ratings = rating_service.calculate_employee_average_rating(emp.emp_id)
        # Ensure avg_ratings is a dictionary and include emp_id
        if isinstance(avg_ratings, dict):
            avg_ratings['emp_id'] = emp.emp_id
            all_avg_ratings_list.append(avg_ratings)
        # Optional: Add logging or warning if unexpected data is returned
        # elif avg_ratings is not None:
        #      st.warning(f"Unexpected return type from calculate_employee_average_rating for employee {emp.emp_id}: {type(avg_ratings)}")


    # Sort employees by overall average rating in descending order to determine rank
    # Handle cases where 'overall' might be missing or None
    ranked_employees_data = sorted(
        all_avg_ratings_list,
        key=lambda x: x.get('overall', 0) if x.get('overall') is not None else -1, # Use 0 or -1 for sorting None values
        reverse=True
    )

    # Create a dictionary for quick lookup of average ratings by emp_id
    avg_ratings_by_id = {item['emp_id']: item for item in all_avg_ratings_list if 'emp_id' in item}

    # Add rank to each employee's data for easy access in the lookup dictionary
    for rank, emp_data in enumerate(ranked_employees_data):
        emp_id = emp_data.get('emp_id')
        if emp_id and emp_id in avg_ratings_by_id: # Ensure the employee data is in the lookup dict
             avg_ratings_by_id[emp_id]['rank'] = rank + 1

    return employees, employee_dict, employee_name_to_id, ranked_employees_data, avg_ratings_by_id

@st.cache_data
def fetch_employee_ratings(employee_id: UUID) -> pd.DataFrame:
     """Fetches detailed ratings for a specific employee and caches it."""
     return pd.DataFrame(rating_service.get_employee_ratings(employee_id))

@st.cache_data
def fetch_employee_comments(employee_id: UUID) -> List[str]:
     """Fetches comments for a specific employee and caches them."""
     return rating_service.get_employee_comments(employee_id)


# --- Main App Layout ---
_, feed_col, _ = st.columns([1, 19, 1])

with feed_col.container(key="employee_container"):

    # Fetch and prepare all necessary employee data once per session
    employees, employee_dict, employee_name_to_id, ranked_employees_data, avg_ratings_by_id = fetch_and_prepare_employee_data()

    # --- Display Top Performers ---
    top_3_employees_data = ranked_employees_data[:3]

    if top_3_employees_data:
        top_1_col, top_2_col, top_3_col = st.columns([1, 1, 1], vertical_alignment="center")
        top_cols = [top_1_col, top_2_col, top_3_col]

        for idx, top_employee_data in enumerate(top_3_employees_data):
            emp_id = top_employee_data.get('emp_id')
            # Use the employee_dict for efficient lookup
            emp = employee_dict.get(emp_id)
            if emp:
                 with top_cols[idx].container(key=f"top_{idx+1}"):
                    st.subheader(f'{emp.first_name} {emp.last_name}')
                    st.markdown(f'Top {idx + 1}')
                    # Safely access overall average rating
                    avg_rating = top_employee_data.get('overall')
                    st.markdown(f'Average Rating: {round(avg_rating, 1) if avg_rating is not None else "N/A"}/5')
    else:
        st.info("No performance data available to show top employees.")


    # --- Tabs for Navigation ---
    by_employee_name_tab, by_office_tab = st.tabs(["Employees", "Offices"])

    with by_employee_name_tab:
        selected_employee_name = st.selectbox(
            'Select Employee',
            options=list(employee_name_to_id.keys()),
            index=None,
            placeholder="Choose an employee..."
        )

        if selected_employee_name:
            # Use the employee_name_to_id dictionary for efficient lookup
            selected_employee_id = employee_name_to_id[selected_employee_name]

            # Fetch detailed data for the selected employee (cached per employee ID)
            employee_ratings_df = fetch_employee_ratings(selected_employee_id)
            # Get pre-calculated average ratings and rank from the cached dictionary
            selected_avg_ratings = avg_ratings_by_id.get(selected_employee_id, {})
            selected_employee_rank = selected_avg_ratings.get('rank', 'N/A')

            if employee_ratings_df.empty:
                st.info("No ratings available for this employee.")
            else:
                # --- Display Metrics ---
                col1, col2, col3 = st.columns(3)

                num_ratings = len(employee_ratings_df)
                # Use pre-fetched overall average rating
                avg_rating = selected_avg_ratings.get('overall', 'N/A')

                with col1:
                    st.metric(label="Number of Ratings", value=num_ratings, border=True)
                with col2:
                     st.metric(label="Average Rating", value=f"{round(avg_rating, 1)}/5" if avg_rating != 'N/A' else 'N/A', border=True)
                with col3:
                    st.metric(label="Rank", value=selected_employee_rank, border=True)

                st.markdown("---") # Separator

                # --- Display Visualizations ---
                st.subheader("Rating Breakdown and Comments")
                col1, col2 = st.columns([2, 1])

                with col1:
                    # Prepare data for the bar chart, excluding 'overall' and 'rank'
                    criteria_avg_ratings = {
                        k: v for k, v in selected_avg_ratings.items()
                        if k.lower() != 'overall' and k != 'rank' and isinstance(v, (int, float)) # Ensure value is numeric
                    }
                    if criteria_avg_ratings:
                        # Pass the prepared dictionary to the visualization function
                        bar_chart_fig = viz.create_bar_chart(criteria_avg_ratings)
                        st.plotly_chart(bar_chart_fig, use_container_width=True)
                    else:
                        st.info("No criteria ratings available for visualization.")

                with col2:
                    # Fetch comments (cached per employee ID)
                    comments = fetch_employee_comments(selected_employee_id)
                    if comments:
                        word_cloud_fig = viz.create_word_cloud(comments)
                        st.pyplot(word_cloud_fig)
                    else:
                        st.info("No comments available to generate a word cloud.")


    with by_office_tab:

        # Select an office
        selected_office = st.selectbox("Select Office", options=list(set(emp.office for emp in employees)), index=None, placeholder="Choose an office...")

        if selected_office:
            # Filter employees by the selected office
            employees_in_office = [emp for emp in employees if emp.office == selected_office]

            # Prepare data for the DataFrame
            data = []
            for emp in employees_in_office:
                emp_id = emp.emp_id
                if emp_id in avg_ratings_by_id:
                    ratings = avg_ratings_by_id[emp_id]
                    num_ratings = len(fetch_employee_ratings(emp_id))
                    
                    # Ensure ratings are floats or set to None
                    criteria_1 = ratings.get('first_criteria')
                    criteria_2 = ratings.get('second_criteria')
                    criteria_3 = ratings.get('third_criteria')
                    criteria_4 = ratings.get('fourth_criteria')
                    
                    data.append({
                        "Name": f"{emp.first_name} {emp.last_name}",
                        "Position": emp.position,
                        "Number of Ratings": num_ratings,
                        "Criteria 1": float(criteria_1) if criteria_1 is not None and isinstance(criteria_1, (int, float)) else 0.0,
                        "Criteria 2": float(criteria_2) if criteria_2 is not None and isinstance(criteria_2, (int, float)) else 0.0,
                        "Criteria 3": float(criteria_3) if criteria_3 is not None and isinstance(criteria_3, (int, float)) else 0.0,
                        "Criteria 4": float(criteria_4) if criteria_4 is not None and isinstance(criteria_4, (int, float)) else 0.0,
                        "Overall Rating": ratings.get('overall', 'N/A')
                    })

            # Create a DataFrame
            df = pd.DataFrame(data)

            # Display the DataFrame using Streamlit's data editor
            st.data_editor(df, use_container_width=True,
                               column_config={
                                   "Criteria 1": st.column_config.ProgressColumn(
                                    "Criteria 1",
                                    help="Criteria 1",
                                    min_value=0,
                                    format="%.1f",
                                    max_value=5,
                                ),
                                    "Criteria 2": st.column_config.ProgressColumn(
                                    "Criteria 2",
                                    help="Criteria 2",
                                    format="%.1f",
                                    min_value=0,
                                    max_value=5,
                                ),
                                    "Criteria 3": st.column_config.ProgressColumn(
                                    "Criteria 3",
                                    help="Criteria 3",
                                    format="%.1f",
                                    min_value=0,
                                    max_value=5,
                                ),
                                    "Criteria 4": st.column_config.ProgressColumn(
                                    "Criteria 4",
                                    help="Criteria 4",
                                    format="%.1f",
                                    min_value=0,
                                    max_value=5,
                                ),
                            },
                            hide_index=True)
            
    st.divider()
    display_footer()


