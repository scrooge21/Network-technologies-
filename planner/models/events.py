from typing import List
from pydantic import BaseModel, Field


class Event(BaseModel):
    id: int = Field(..., description="Уникальный номер события")
    title: str = Field(..., description="Название события")
    image: str = Field(..., description="Ссылка на баннер события")
    description: str = Field(..., description="Описание события")
    tags: List[str] = Field(..., description="Теги для группировки событий")
    location: str = Field(..., description="Место проведения")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event.",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet",
            }
        }
    }