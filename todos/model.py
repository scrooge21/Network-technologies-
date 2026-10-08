from typing import List, Optional
from fastapi import Form
from pydantic import BaseModel, Field


class Todo(BaseModel):
    id: Optional[int] = None
    item: str

    @classmethod
    def as_form(cls, item: str = Form(...)):
        return cls(item=item)

    model_config = {
        "json_schema_extra": {
            "example": {"id": 1, "item": "Example schema!"}
        }
    }


class TodoItem(BaseModel):
    item: str

    model_config = {
        "json_schema_extra": {
            "example": {"item": "Read the next chapter of the book"}
        }
    }


class TodoItems(BaseModel):
    todos: List[TodoItem]


class BookCreate(BaseModel):
    id: int
    title: str = Field(..., min_length=2)
    author: str = Field(..., min_length=2)
    year: int = Field(..., ge=1450, le=2026)
    copies: int = Field(1, ge=1)


class Book(BookCreate):
    borrowed: int = 0


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    year: int
    available: int