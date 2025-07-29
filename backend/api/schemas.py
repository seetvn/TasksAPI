from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models import TaskStatus

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime

class TaskUpdate(BaseModel):
    status: TaskStatus
