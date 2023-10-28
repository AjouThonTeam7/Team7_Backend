from pydantic import BaseModel
from typing import List, Optional


# class EmptyTimeSchema(BaseModel):
#     user_id: int
#     weekday: str  # e.g., 'Monday'
#     periods: List[str]  # List of periods e.g., ['A', 'B', 'C']

#     class Config:
#         orm_mode = True
class CreateUser(BaseModel):
    user_id: str
    user_pw: str


class UserSchema(BaseModel):
    user_id: str
    user_pw: str
    user_name: str
    major: str
    subjects: List[str]
    # empty_times: List[EmptyTimeSchema]  # Updated to use EmptyTimeSchema

    class Config:
        orm_mode = True
