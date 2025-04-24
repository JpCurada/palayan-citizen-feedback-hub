from core.db import supabase
from models.models import Client
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class ClientRepository:
    def __init__(self):
        self.table_name = "clients"
    
    def get_all(self) -> List[Client]:
        response = supabase.table(self.table_name).select("*").execute()
        return [Client.from_dict(item) for item in response.data]
    
    def get_by_id(self, client_id: UUID) -> Optional[Client]:
        response = supabase.table(self.table_name).select("*").eq("client_id", str(client_id)).execute()
        return Client.from_dict(response.data[0]) if response.data else None
    
    def create(self, client: Client) -> Optional[Client]:
        client_dict = client.to_dict()
        
        # Set created_at timestamp if not already set
        if client_dict.get("created_at") is None:
            client_dict["created_at"] = datetime.now().isoformat()
            
        response = supabase.table(self.table_name).insert(client_dict).execute()
        return Client.from_dict(response.data[0]) if response.data else None
    
    def update(self, client: Client) -> Optional[Client]:
        response = supabase.table(self.table_name).update(client.to_dict()).eq("client_id", str(client.client_id)).execute()
        return Client.from_dict(response.data[0]) if response.data else None
    
    def delete(self, client_id: UUID) -> bool:
        response = supabase.table(self.table_name).delete().eq("client_id", str(client_id)).execute()
        return len(response.data) > 0
    