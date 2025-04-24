from core.db import supabase
from models.models import Admin
from typing import List, Optional
from uuid import UUID


class AdminRepository:
    def __init__(self):
        self.table_name = "admins"
    
    def get_all(self) -> List[Admin]:
        response = supabase.table(self.table_name).select("*").execute()
        return [Admin.from_dict(item) for item in response.data]
    
    def get_by_id(self, admin_id: UUID) -> Optional[Admin]:
        response = supabase.table(self.table_name).select("*").eq("admin_id", str(admin_id)).execute()
        return Admin.from_dict(response.data[0]) if response.data else None
    
    def create(self, admin: Admin) -> Optional[Admin]:
        response = supabase.table(self.table_name).insert(admin.to_dict()).execute()
        return Admin.from_dict(response.data[0]) if response.data else None
    
    def update(self, admin: Admin) -> Optional[Admin]:
        response = supabase.table(self.table_name).update(admin.to_dict()).eq("admin_id", str(admin.admin_id)).execute()
        return Admin.from_dict(response.data[0]) if response.data else None
    
    def delete(self, admin_id: UUID) -> bool:
        response = supabase.table(self.table_name).delete().eq("admin_id", str(admin_id)).execute()
        return len(response.data) > 0

    def get_by_email(self, email: str) -> Optional[Admin]:
        response = supabase.table(self.table_name).select("*").eq("email_address", email).execute()
        return Admin.from_dict(response.data[0]) if response.data else None


# Similar repositories for Client, Queue, and Rating
# app/repositories/client_repository.py, queue_repository.py, rating_repository.py
# Follow the same pattern as above