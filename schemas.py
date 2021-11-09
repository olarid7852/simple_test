from enum import Enum
from typing import Optional
from pydantic import BaseModel, ValidationError, validator
from models import Member as MemberModel


class Member(BaseModel):
    team_id: int
    name: str
    age: int
    id: Optional[int]


    @staticmethod
    def from_model_object(object: MemberModel):
        return Member(team_id=object.team_id, age=object.age, name=object.name, id=object.id) 

    @validator('age')
    def age_must_be_greater_than_9(cls, v):
        if v < 10:
            raise ValueError('Age must be greater than or equal to 10')
        return v

    @validator('name')
    def name_must_be_longer_than_4(cls, v):
        if len(v) < 5:
            raise ValueError('Name must be longer than 4')
        return v
