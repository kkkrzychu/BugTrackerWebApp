from pydantic import BaseModel
from datetime import datetime

class BugCreate(BaseModel):
    title: str
    description: str
    priority: str

class BugResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime

class BugUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: str | None = None