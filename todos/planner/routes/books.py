from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database.connection import get_session
from models.books import Book, BookUpdate

book_router = APIRouter(tags=["Books"])


@book_router.get("/", response_model=List[Book], summary="Список всех книг",
                 description="Возвращает все книги из базы данных.")
async def retrieve_all_books(session: Session = Depends(get_session)) -> List[Book]:
    return session.exec(select(Book)).all()


@book_router.get("/{id}", response_model=Book, summary="Получить книгу по ID",
                 responses={404: {"description": "Книга с таким ID не найдена"}})
async def retrieve_book(id: int, session: Session = Depends(get_session)) -> Book:
    book = session.get(Book, id)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book with supplied ID does not exist")


@book_router.post("/new", summary="Добавить книгу",
                  description="Добавляет книгу в базу. ID назначается автоматически.")
async def create_book(new_book: Book, session: Session = Depends(get_session)) -> dict:
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return {"message": "Book created successfully", "id": new_book.id}


@book_router.put("/edit/{id}", response_model=Book, summary="Изменить книгу",
                 description="Меняет только те поля, которые переданы в теле запроса.",
                 responses={404: {"description": "Книга с таким ID не найдена"}})
async def update_book(id: int, new_data: BookUpdate, session: Session = Depends(get_session)) -> Book:
    book = session.get(Book, id)
    if book:
        for key, value in new_data.model_dump(exclude_unset=True).items():
            setattr(book, key, value)
        session.add(book)
        session.commit()
        session.refresh(book)
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book with supplied ID does not exist")


@book_router.delete("/delete/{id}", summary="Удалить книгу по ID",
                    responses={404: {"description": "Книга с таким ID не найдена"}})
async def delete_book(id: int, session: Session = Depends(get_session)) -> dict:
    book = session.get(Book, id)
    if book:
        session.delete(book)
        session.commit()
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book with supplied ID does not exist")