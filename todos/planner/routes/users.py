from fastapi import APIRouter, HTTPException, status
from models.users import NewUser, UserSignIn

user_router = APIRouter(tags=["User"])

users = {}


@user_router.post(
    "/signup",
    summary="Регистрация пользователя",
    description="Создаёт нового пользователя. Почта должна быть уникальной.",
    responses={409: {"description": "Пользователь с такой почтой уже существует"}},
)
async def sign_new_user(data: NewUser) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied email exists",
        )
    users[data.email] = data
    return {"message": "User successfully registered!"}


@user_router.post(
    "/signin",
    summary="Вход пользователя",
    description="Проверяет почту и пароль. Сначала нужно зарегистрироваться через /signup.",
    responses={
        404: {"description": "Пользователь не найден"},
        403: {"description": "Неверный пароль"},
    },
)
async def sign_user_in(user: UserSignIn) -> dict:
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed",
        )
    return {"message": "User signed in successfully"}


@user_router.post(
    "/signout",
    summary="Выход пользователя",
    description="Завершает сессию пользователя (в учебной версии возвращает только сообщение).",
)
async def sign_user_out() -> dict:
    return {"message": "User signed out successfully"}