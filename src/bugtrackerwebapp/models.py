from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal

class BugBase(BaseModel):
    
    @field_validator("title", "description", mode="before", check_fields=False)
    @classmethod
    def strip_text(cls, value):
        if isinstance(value, str):
            return value.strip()

        return value
    
class BugCreate(BugBase):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5)
    priority: Literal["Low", "Medium", "High"]

class BugResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime

class BugUpdate(BugBase):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, min_length=5)
    priority: Literal["Low", "Medium", "High"] | None = None

