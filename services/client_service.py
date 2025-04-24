from repositories.client_repository import ClientRepository
from services.queue_service import QueueService
from models.models import Client
from typing import List, Optional, Tuple
from uuid import UUID


class ClientService:
    def __init__(self):
        self.repository = ClientRepository()
        self.queue_service = QueueService()
    
    def get_all_clients(self) -> List[Client]:
        return self.repository.get_all()
    
    def get_client_by_id(self, client_id: UUID) -> Optional[Client]:
        return self.repository.get_by_id(client_id)
    
    def create_client(self, client: Client) -> Tuple[Optional[Client], Optional[int]]:
        """
        Creates a client and assigns them a queue number
        Returns a tuple of (client, queue_id)
        """
        # Create the client
        created_client = self.repository.create(client)
        
        if created_client:
            # Create a queue for the client
            queue = self.queue_service.create_queue(created_client.client_id)
            if queue:
                return created_client, queue.queue_id
        
        return created_client, None
    
    def update_client(self, client: Client) -> Optional[Client]:
        return self.repository.update(client)
    
    def delete_client(self, client_id: UUID) -> bool:
        return self.repository.delete(client_id)
    
