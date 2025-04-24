from repositories.queue_repository import QueueRepository
from models.models import Queue
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class QueueService:
    def __init__(self):
        self.repository = QueueRepository()
    
    def get_all_queues(self) -> List[Queue]:
        return self.repository.get_all()
    
    def get_active_queues(self) -> List[Queue]:
        response = self.repository.get_active_queues()
        return response
    
    def create_queue(self, client_id: UUID) -> Optional[Queue]:
        queue = Queue(client_id=client_id)
        return self.repository.create(queue)
    
    def end_queue(self, queue_id: int) -> Optional[Queue]:
        queue = self.repository.get_by_id(queue_id)
        if queue:
            queue.ended_at = datetime.now()
            return self.repository.update(queue)
        return None
    
    def get_client_queues(self, client_id: UUID) -> List[Queue]:
        return self.repository.get_by_client_id(client_id)
    
    def get_queue_by_id(self, queue_id: int) -> Optional[Queue]:
        return self.repository.get_by_id(queue_id)
    
    def get_pending_queues(self) -> List[Queue]:
        """Get all pending queues (active queues that have not ended)"""
        return self.get_active_queues()

