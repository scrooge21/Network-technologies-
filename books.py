from typing import List, Optional
from fastapi import APIRouter
from model import BookCreate, Book, BookOut

books_router = APIRouter(prefix="/books", tags=["books"])
books = []


class LibraryError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


def find_book(book_id: int) -> Book:
    for b in books:
        if b.id == book_id:
            return b
    raise LibraryError(404, f"Книга с ID {book_id} не найдена")


def to_out(b: Book) -> BookOut:
    return BookOut(id=b.id, title=b.title, author=b.author,
                   year=b.year, available=b.copies - b.borrowed)


@books_router.post("", status_code=201)
async def add_book(data: BookCreate) -> dict:
    if any(b.id == data.id for b in books):
        raise LibraryError(400, "Книга с таким ID уже существует")
    books.append(Book(**data.model_dump()))
    return {"message": "Книга добавлена в библиотеку. Разработчик: Ринар"}


@books_router.get("", response_model=List[BookOut])
async def list_books(author: Optional[str] = None,
                     only_available: bool = False):
    result = books
    if author:
        result = [b for b in result if author.lower() in b.author.lower()]
    if only_available:
        result = [b for b in result if b.copies - b.borrowed > 0]
    if not result:
        raise LibraryError(404, "По заданным условиям книг не найдено")
    return [to_out(b) for b in result]


@books_router.get("/stats")
async def stats() -> dict:
    return {
        "titles": len(books),
        "copies_total": sum(b.copies for b in books),
        "borrowed_now": sum(b.borrowed for b in books),
    }


@books_router.post("/{book_id}/borrow")
async def borrow_book(book_id: int) -> dict:
    b = find_book(book_id)
    if b.borrowed >= b.copies:
        raise LibraryError(409, "Свободных экземпляров нет")
    b.borrowed += 1
    return {"message": "Книга выдана", "available": b.copies - b.borrowed}


@books_router.post("/{book_id}/return")
async def return_book(book_id: int) -> dict:
    b = find_book(book_id)
    if b.borrowed == 0:
        raise LibraryError(409, "Эта книга не выдавалась")
    b.borrowed -= 1
    return {"message": "Книга принята", "available": b.copies - b.borrowed}


@books_router.delete("/{book_id}")
async def delete_book(book_id: int) -> dict:
    b = find_book(book_id)
    if b.borrowed > 0:
        raise LibraryError(409, "Нельзя удалить: есть выданные экземпляры")
    books.remove(b)
    return {"message": "Книга удалена"}