from repositories.admin_repository import AdminRepository
from models.models import Admin
from typing import List, Optional
from uuid import UUID


class AdminService:
    def __init__(self):
        self.repository = AdminRepository()
    
    def get_all_admins(self) -> List[Admin]:
        return self.repository.get_all()
    
    def get_admin_by_id(self, admin_id: UUID) -> Optional[Admin]:
        return self.repository.get_by_id(admin_id)
    
    def create_admin(self, admin: Admin) -> Optional[Admin]:
        return self.repository.create(admin)
    
    def update_admin(self, admin: Admin) -> Optional[Admin]:
        return self.repository.update(admin)
    
    def delete_admin(self, admin_id: UUID) -> bool:
        return self.repository.delete(admin_id)
    
    def get_admin_by_email(self, email: str) -> Optional[Admin]:
        return self.repository.get_by_email(email)
