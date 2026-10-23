from typing import Optional
from sqlmodel import SQLModel, Field


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="Номер книги (назначается базой)")
    title: str = Field(description="Название книги")
    author: str = Field(description="Автор")
    year: int = Field(description="Год издания")
    available: bool = Field(default=True, description="Есть ли книга в наличии")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Мастер и Маргарита",
                "author": "М. А. Булгаков",
                "year": 1967,
                "available": True,
            }
        }
    }


class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    available: Optional[bool] = None

    model_config = {
        "json_schema_extra": {"example": {"available": False}}
    }