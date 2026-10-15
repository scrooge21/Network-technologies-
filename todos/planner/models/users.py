from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from models.events import Event


class User(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта (используется как логин)")
    username: str = Field(..., description="Имя пользователя")
    events: Optional[List[Event]] = Field([], description="События, созданные пользователем")


class NewUser(User):
    password: str = Field(..., description="Пароль пользователя")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "fastapi@packt.com",
                "username": "FastPackt",
                "password": "Stro0ng!",
                "events": [],
            }
        }
    }


class UserSignIn(BaseModel):
    email: EmailStr = Field(..., description="Почта, указанная при регистрации")
    password: str = Field(..., description="Пароль пользователя")

    model_config = {
        "json_schema_extra": {
            "example": {"email": "fastapi@packt.com", "password": "Stro0ng!"}
        }
    }