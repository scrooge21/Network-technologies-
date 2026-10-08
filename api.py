from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from todo import todo_router
from books import books_router, LibraryError

app = FastAPI()


@app.exception_handler(LibraryError)
async def library_error_handler(request: Request, exc: LibraryError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "status": exc.status_code},
    )


@app.get("/")
async def welcome() -> dict:
    return {"message": "Привет, Ринар!"}


app.include_router(todo_router)
app.include_router(books_router)