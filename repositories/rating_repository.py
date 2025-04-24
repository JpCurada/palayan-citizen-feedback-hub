from core.db import supabase
from models.models import Rating
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class RatingRepository:
    def __init__(self):
        self.table_name = "ratings"
    
    def get_all(self) -> List[Rating]:
        response = supabase.table(self.table_name).select("*").execute()
        return [Rating.from_dict(item) for item in response.data]
    
    def get_by_id(self, rating_id: UUID) -> Optional[Rating]:
        response = supabase.table(self.table_name).select("*").eq("rating_id", str(rating_id)).execute()
        return Rating.from_dict(response.data[0]) if response.data else None
    
    def create(self, rating: Rating) -> Optional[Rating]:
        # Remove rating_id if it's None to let the database generate it
        rating_dict = rating.to_dict()
        if rating_dict["rating_id"] is None:
            del rating_dict["rating_id"]
        
        # Set created_at timestamp if not already set
        if rating_dict.get("created_at") is None:
            rating_dict["created_at"] = datetime.now().isoformat()
            
        response = supabase.table(self.table_name).insert(rating_dict).execute()
        return Rating.from_dict(response.data[0]) if response.data else None
    
    def update(self, rating: Rating) -> Optional[Rating]:
        response = supabase.table(self.table_name).update(rating.to_dict()).eq("rating_id", str(rating.rating_id)).execute()
        return Rating.from_dict(response.data[0]) if response.data else None
    
    def delete(self, rating_id: UUID) -> bool:
        response = supabase.table(self.table_name).delete().eq("rating_id", str(rating_id)).execute()
        return len(response.data) > 0
    
    def get_by_employee_id(self, emp_id: UUID) -> List[Rating]:
        response = supabase.table(self.table_name).select("*").eq("emp_id", str(emp_id)).execute()
        return [Rating.from_dict(item) for item in response.data]
    
    def get_by_queue_id(self, queue_id: int) -> List[Rating]:
        response = supabase.table(self.table_name).select("*").eq("queue_id", queue_id).execute()
        return [Rating.from_dict(item) for item in response.data]
    
    def get_average_ratings_by_employee(self, emp_id: UUID) -> dict:
        # This would typically be a more complex query in SQL
        # For Supabase, we'll fetch the data and calculate in Python
        ratings = self.get_by_employee_id(emp_id)
        
        if not ratings:
            return {
                "first_criteria": 0,
                "second_criteria": 0,
                "third_criteria": 0,
                "fourth_criteria": 0,
                "overall": 0
            }
        
        total_first = sum(r.first_criteria for r in ratings if r.first_criteria is not None)
        total_second = sum(r.second_criteria for r in ratings if r.second_criteria is not None)
        total_third = sum(r.third_criteria for r in ratings if r.third_criteria is not None)
        total_fourth = sum(r.fourth_criteria for r in ratings if r.fourth_criteria is not None)
        
        count_first = sum(1 for r in ratings if r.first_criteria is not None)
        count_second = sum(1 for r in ratings if r.second_criteria is not None)
        count_third = sum(1 for r in ratings if r.third_criteria is not None)
        count_fourth = sum(1 for r in ratings if r.fourth_criteria is not None)
        
        return {
            "first_criteria": total_first / count_first if count_first > 0 else 0,
            "second_criteria": total_second / count_second if count_second > 0 else 0,
            "third_criteria": total_third / count_third if count_third > 0 else 0,
            "fourth_criteria": total_fourth / count_fourth if count_fourth > 0 else 0,
            "overall": (
                (total_first / count_first if count_first > 0 else 0) +
                (total_second / count_second if count_second > 0 else 0) +
                (total_third / count_third if count_third > 0 else 0) +
                (total_fourth / count_fourth if count_fourth > 0 else 0)
            ) / 4
        }
    
    def get_comments_by_employee_id(self, emp_id: UUID) -> List[str]:
        response = supabase.table(self.table_name).select("comments").eq("emp_id", str(emp_id)).execute()
        return [item['comments'] for item in response.data if item['comments']]