# app/models/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID as PyUUID

@dataclass
class Admin:
    admin_id: PyUUID
    email_address: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self):
        return {
            "admin_id": str(self.admin_id),
            "email_address": self.email_address,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        if "admin_id" in data and data["admin_id"]:
            data["admin_id"] = PyUUID(data["admin_id"])
        return cls(**data)

@dataclass
class Employee:
    emp_id: PyUUID
    first_name: str
    last_name: str
    office: Optional[str] = None
    position: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self):
        return {
            "emp_id": str(self.emp_id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "office": self.office,
            "position": self.position,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        if "emp_id" in data and data["emp_id"]:
            data["emp_id"] = PyUUID(data["emp_id"])
        return cls(**data)

@dataclass
class Client:
    client_id: PyUUID
    first_name: str
    last_name: str
    created_at: Optional[datetime] = None
    
    def to_dict(self):
        return {
            "client_id": str(self.client_id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        if "client_id" in data and data["client_id"]:
            data["client_id"] = PyUUID(data["client_id"])
        return cls(**data)

@dataclass
class Queue:
    queue_id: Optional[int] = None
    client_id: Optional[PyUUID] = None
    created_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    
    def to_dict(self):
        return {
            "queue_id": self.queue_id,
            "client_id": str(self.client_id) if self.client_id else None,
            "created_at": self.created_at,
            "ended_at": self.ended_at
        }
    
    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        if "client_id" in data and data["client_id"]:
            data["client_id"] = PyUUID(data["client_id"])
        return cls(**data)

@dataclass
class Rating:
    rating_id: Optional[PyUUID] = None
    queue_id: Optional[int] = None
    emp_id: Optional[PyUUID] = None
    first_criteria: Optional[int] = None
    second_criteria: Optional[int] = None
    third_criteria: Optional[int] = None
    fourth_criteria: Optional[int] = None
    comments: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self):
        return {
            "rating_id": str(self.rating_id) if self.rating_id else None,
            "queue_id": self.queue_id,
            "emp_id": str(self.emp_id) if self.emp_id else None,
            "first_criteria": self.first_criteria,
            "second_criteria": self.second_criteria,
            "third_criteria": self.third_criteria,
            "fourth_criteria": self.fourth_criteria,
            "comments": self.comments,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        if "rating_id" in data and data["rating_id"]:
            data["rating_id"] = PyUUID(data["rating_id"])
        if "emp_id" in data and data["emp_id"]:
            data["emp_id"] = PyUUID(data["emp_id"])
        return cls(**data)

class Office:
    def __init__(self, office_id: PyUUID, name: str):
        self.office_id = office_id
        self.name = name

    @staticmethod
    def from_dict(data: dict) -> 'Office':
        return Office(
            office_id=PyUUID(data['office_id']),
            name=data['name']
        )

    def to_dict(self) -> dict:
        return {
            'office_id': str(self.office_id),
            'name': self.name
        }