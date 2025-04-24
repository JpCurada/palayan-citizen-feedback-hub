from core.db import supabase
from models.models import Queue
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class QueueRepository:
    def __init__(self):
        self.table_name = "queues"
    
    def get_all(self) -> List[Queue]:
        response = supabase.table(self.table_name).select("*").execute()
        return [Queue.from_dict(item) for item in response.data]
    
    def get_by_id(self, queue_id: int) -> Optional[Queue]:
        response = supabase.table(self.table_name).select("*").eq("queue_id", queue_id).execute()
        return Queue.from_dict(response.data[0]) if response.data else None
    
    def create(self, queue: Queue) -> Optional[Queue]:
        # Remove queue_id if it's None to let the database generate it
        queue_dict = queue.to_dict()
        if queue_dict["queue_id"] is None:
            del queue_dict["queue_id"]
        
        # Set created_at timestamp if not already set
        if queue_dict.get("created_at") is None:
            queue_dict["created_at"] = datetime.now().isoformat()
        
        response = supabase.table(self.table_name).insert(queue_dict).execute()
        return Queue.from_dict(response.data[0]) if response.data else None
    
    def update(self, queue: Queue) -> Optional[Queue]:
        # Ensure timestamps are in ISO format
        queue_dict = queue.to_dict()
        if queue_dict.get("ended_at") is not None and not isinstance(queue_dict["ended_at"], str):
            queue_dict["ended_at"] = queue_dict["ended_at"].isoformat()
            
        response = supabase.table(self.table_name).update(queue_dict).eq("queue_id", queue.queue_id).execute()
        return Queue.from_dict(response.data[0]) if response.data else None
    
    def delete(self, queue_id: int) -> bool:
        response = supabase.table(self.table_name).delete().eq("queue_id", queue_id).execute()
        return len(response.data) > 0
    
    def get_active_queues(self) -> List[Queue]:
        response = supabase.table(self.table_name).select("*").is_("ended_at", "null").execute()
        return [Queue.from_dict(item) for item in response.data]
    
    def get_by_client_id(self, client_id: UUID) -> List[Queue]:
        response = supabase.table(self.table_name).select("*").eq("client_id", str(client_id)).execute()
        return [Queue.from_dict(item) for item in response.data]
    
    def get_queues_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Queue]:
        response = supabase.table(self.table_name).select("*").gte("created_at", start_date.isoformat()).lte("created_at", end_date.isoformat()).execute()
        return [Queue.from_dict(item) for item in response.data]