from repositories.employee_repository import EmployeeRepository
from repositories.office_repository import OfficeRepository
from models.models import Employee, Office
from typing import List, Optional, Dict, Any
from uuid import UUID


class EmployeeService:
    def __init__(self):
        self.repository = EmployeeRepository()
        self.office_repository = OfficeRepository()
    
    def get_all_employees(self) -> List[Employee]:
        return self.repository.get_all()
    
    def get_employee_by_id(self, emp_id: UUID) -> Optional[Employee]:
        return self.repository.get_by_id(emp_id)
    
    def create_employee(self, employee: Employee) -> Optional[Employee]:
        return self.repository.create(employee)
    
    def update_employee(self, employee: Employee) -> Optional[Employee]:
        return self.repository.update(employee)
    
    def delete_employee(self, emp_id: UUID) -> bool:
        return self.repository.delete(emp_id)
    
    def get_employees_by_office(self, office_id: UUID) -> List[Employee]:
        return self.repository.get_by_office(office_id)

    def get_employees_by_office_name(self, office_name: str) -> List[Employee]:
        return self.repository.get_by_office_name(office_name)

    def calculate_office_metrics(self, office_id: UUID) -> Dict[str, Any]:
        employees = self.get_employees_by_office(office_id)
        num_employees = len(employees)
        if num_employees == 0:
            return {
                "num_employees": 0,
                "average_rating": "N/A",
                "rank": "N/A"
            }
        total_ratings = 0
        total_avg_rating = 0
        for emp in employees:
            avg_ratings = self.rating_service.calculate_employee_average_rating(emp.emp_id)
            total_avg_rating += avg_ratings['overall']
            total_ratings += 1 if avg_ratings['overall'] > 0 else 0
        average_rating = total_avg_rating / total_ratings if total_ratings > 0 else "N/A"
        # Rank calculation logic can be added here
        return {
            "num_employees": num_employees,
            "average_rating": average_rating,
            "rank": "N/A"  # Placeholder for rank
        }
    
    def get_all_offices(self) -> List[Office]:
        return self.office_repository.get_all()
    