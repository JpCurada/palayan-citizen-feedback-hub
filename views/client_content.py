import streamlit as st
import uuid
import time

from services.client_service import ClientService
from services.queue_service import QueueService
from services.rating_service import RatingService
from services.employee_service import EmployeeService
from models.models import Client

from components.footer import display_footer

# Initialize services
client_service = ClientService()
queue_service = QueueService()
rating_service = RatingService()
employee_service = EmployeeService()

# Define the dialog outside any fragment
@st.dialog(title="Rating Form")
def rating_form(queue_obj):
    # Add empty elements to avoid stale elements from previous dialogs
    for _ in range(10):
        st.empty()
    st.info(f"Queue Number: {queue_obj.queue_id}")
    st.write("Please rate the employee based on your experience.")

    # Fetch employees from the database
    employees = employee_service.get_all_employees()
    employee_dict = {f"{emp.first_name} {emp.last_name}, {emp.position}": emp.emp_id for emp in employees}
    
    # Display employee selection
    selected_employee_name = st.selectbox("Select Employee", list(employee_dict.keys()))
    selected_employee_id = employee_dict[selected_employee_name]
    
    # Rating scale
    first_criteria = st.slider("First Criteria", 1, 5, 3)
    second_criteria = st.slider("Second Criteria", 1, 5, 3)
    third_criteria = st.slider("Third Criteria", 1, 5, 3)
    fourth_criteria = st.slider("Fourth Criteria", 1, 5, 3)
    
    average_rating = (first_criteria + second_criteria + third_criteria + fourth_criteria) / 4
    
    comments = st.text_area("Comments")
    
    # Submit button
    if st.button("Submit Rating"):
        # Handle rating logic here
        criteria = {
            'first': first_criteria,
            'second': second_criteria,
            'third': third_criteria,
            'fourth': fourth_criteria
        }
        rating_service.create_rating(queue_obj.queue_id, selected_employee_id, criteria, comments)
        st.success(
            f"Thank you for rating {selected_employee_name}. Your feedback is highly appreciated."
        )
        st.markdown("---")
        st.caption(f"Don't forget to end your queue ({queue_obj.queue_id}) to avoid inconvenience for the next person in line.")
        st.balloons()


_, feed_col, _ = st.columns([1, 2, 1])
with feed_col.container(key="form_container_1"):
    st.subheader("Welcome, Client!")
    st.markdown("Please fill out the form below to get a **queue number** and **start rating employees**.")

    # Registration form as a fragment
    @st.fragment
    def registration_form():
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        
        register_col, end_col = st.columns([2,1])

        with register_col:
            submit_button = st.button(
                label="Get Queue Number", 
                disabled=True if not first_name or not last_name else False,
                use_container_width=True
            )

        with end_col:
            back_button = st.button(
                label="End Queue" if "registered_queue_id" in st.session_state else "Back",
                use_container_width=True
            )
        
        if submit_button:
            # Handle registration logic here
            client_id = uuid.uuid4()
            client = Client(client_id=client_id, first_name=first_name, last_name=last_name)
            created_client, queue_id = client_service.create_client(client)
            if created_client:
                queue = queue_service.create_queue(created_client.client_id)
                if queue:
                    st.session_state.registered_queue_id = queue.queue_id
                    rating_form(queue_obj = queue)  # Open the dialog
                else:
                    st.error("Failed to create a queue number.")
            else:
                st.error("Failed to register client.")

        if back_button:
            if "registered_queue_id" in st.session_state:
                queue_service.end_queue(st.session_state.registered_queue_id)
                del st.session_state.registered_queue_id
            st.switch_page("views/user_content.py")

    registration_form()

    
