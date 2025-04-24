from repositories.rating_repository import RatingRepository
from models.models import Rating
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime


class RatingService:
    def __init__(self):
        self.repository = RatingRepository()
    
    def get_all_ratings(self) -> List[Rating]:
        return self.repository.get_all()
    
    def get_rating_by_id(self, rating_id: UUID) -> Optional[Rating]:
        return self.repository.get_by_id(rating_id)
    
    def create_rating(self, queue_id: int, emp_id: UUID, criteria: Dict[str, int], comments: str = None) -> Optional[Rating]:
        rating = Rating(
            queue_id=queue_id,
            emp_id=emp_id,
            first_criteria=criteria.get('first', None),
            second_criteria=criteria.get('second', None),
            third_criteria=criteria.get('third', None),
            fourth_criteria=criteria.get('fourth', None),
            comments=comments
        )
        return self.repository.create(rating)
    
    def get_employee_ratings(self, emp_id: UUID) -> List[Rating]:
        return self.repository.get_by_employee_id(emp_id)
    
    def get_queue_ratings(self, queue_id: int) -> List[Rating]:
        return self.repository.get_by_queue_id(queue_id)
    
    def calculate_employee_average_rating(self, emp_id: UUID) -> Dict[str, float]:
        ratings = self.get_employee_ratings(emp_id)
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
        
        avg_first = total_first / count_first if count_first > 0 else 0
        avg_second = total_second / count_second if count_second > 0 else 0
        avg_third = total_third / count_third if count_third > 0 else 0
        avg_fourth = total_fourth / count_fourth if count_fourth > 0 else 0
        
        overall = (avg_first + avg_second + avg_third + avg_fourth) / 4
        
        return {
            "first_criteria": avg_first,
            "second_criteria": avg_second,
            "third_criteria": avg_third,
            "fourth_criteria": avg_fourth,
            "overall": overall
        }
    
    def get_employee_comments(self, emp_id: UUID) -> List[str]:
        return self.repository.get_comments_by_employee_id(emp_id)
    
    def get_top_employees(self, employees: List[UUID]) -> List[Dict[str, Any]]:
        employee_ratings = []
        for emp_id in employees:
            avg_ratings = self.calculate_employee_average_rating(emp_id)
            if avg_ratings['overall'] > 0:  # Only consider employees with ratings
                employee_ratings.append({'emp_id': emp_id, 'average_rating': avg_ratings['overall']})
        # Sort employees by average rating in descending order
        employee_ratings.sort(key=lambda x: x['average_rating'], reverse=True)
        # Return top 3 employees
        return employee_ratings[:3]