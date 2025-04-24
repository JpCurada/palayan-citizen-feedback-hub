from core.db import supabase
from models.models import Employee
from typing import List, Optional
from uuid import UUID


class EmployeeRepository:
    def __init__(self):
        self.table_name = "employees"
    
    def get_all(self) -> List[Employee]:
        response = supabase.table(self.table_name).select("*").execute()
        return [Employee.from_dict(item) for item in response.data]
    
    def get_by_id(self, emp_id: UUID) -> Optional[Employee]:
        response = supabase.table(self.table_name).select("*").eq("emp_id", str(emp_id)).execute()
        return Employee.from_dict(response.data[0]) if response.data else None
    
    def create(self, employee: Employee) -> Optional[Employee]:
        response = supabase.table(self.table_name).insert(employee.to_dict()).execute()
        return Employee.from_dict(response.data[0]) if response.data else None
    
    def update(self, employee: Employee) -> Optional[Employee]:
        response = supabase.table(self.table_name).update(employee.to_dict()).eq("emp_id", str(employee.emp_id)).execute()
        return Employee.from_dict(response.data[0]) if response.data else None
    
    def delete(self, emp_id: UUID) -> bool:
        response = supabase.table(self.table_name).delete().eq("emp_id", str(emp_id)).execute()
        return len(response.data) > 0
    
