from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal

class BugCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5)
    priority: Literal["Low", "Medium", "High"]

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value):
        if isinstance(value, str):
            return value.strip()

        return value

    @field_validator("description", mode="before")
    @classmethod
    def validate_description(cls, value):
        if isinstance(value, str):
            return value.strip()

        return value

class BugResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime

class BugUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, min_length=5)
    priority: Literal["Low", "Medium", "High"] | None = None