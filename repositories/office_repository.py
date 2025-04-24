from core.db import supabase
from models.models import Office
from typing import List
from uuid import UUID


class OfficeRepository:
    def __init__(self):
        self.table_name = "offices"

    def get_all(self) -> List[Office]:
        response = supabase.table(self.table_name).select("*").execute()
        return [Office.from_dict(item) for item in response.data] 