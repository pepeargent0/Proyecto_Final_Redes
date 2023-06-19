import json
import logging
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import BaseModel, validator

app = FastAPI()
logger = logging.getLogger(__name__)


class Book(BaseModel):
    author: str
    country: str
    imageLink: str
    language: str
    link: str
    pages: int
    title: str
    year: int

    @validator('*')
    def validate_fields(cls, field):
        if not field:
            raise ValueError("Todos los campos son requeridos")
        return field


class ResponseBook(BaseModel):
    status: str
    books: list | dict
    count: int


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(content={"error": "HTTP exception"}, status_code=exc.status_code)


def read_books_file():
    file_path = "source/books.json"
    try:
        with open(file_path, "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        books = []
    return books


def write_books_file(books):
    file_path = "source/books.json"
    try:
        with open(file_path, "w") as file:
            json.dump(books, file, indent=4)
    except Exception as e:
        logger.error(f"Error writing books file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/")
async def info():
    """
    Ruta para obtener información de la versión de la API.
    """
    return {"version": "0.0.1"}


@app.get("/books")
async def get_books(country: str = None, language: str = None, author: str = None, year: int = None):
    """
    Ruta para obtener la lista de libros desde un archivo JSON.
    """
    books = read_books_file()

    filtered_books = [book for book in books
                      if (not author or book['author'] == author)
                      and (not language or book['language'] == language)
                      and (not year or book['year'] == year)
                      and (not country or book['country'] == country)]

    response = ResponseBook(
        status="success",
        books=filtered_books,
        count=len(filtered_books)
    )
    return JSONResponse(content=response.dict(), status_code=200)


@app.post("/books")
async def create_book(book: Book):
    books = read_books_file()
    books.append(book.dict())
    write_books_file(books)

    response = ResponseBook(
        status="success",
        books=book.dict(),
        count=1
    )
    return JSONResponse(content=response.dict(), status_code=201)


@app.delete("/books")
async def delete_book(author: str = None, year: int = None, country: str = None, title: str = None,
                      language: str = None):
    books = read_books_file()

    if author is None and year is None and country is None and title is None and language is None:
        write_books_file([])
        response = ResponseBook(
            status="success",
            books=[],
            count=0
        )
        return JSONResponse(content=response.dict(), status_code=200)

    filtered_books = [book for book in books
                      if (not author or book['author'] != author)
                      or (not year or book['year'] != year)
                      or (not country or book['country'] != country)
                      or (not title or book['title'] != title)
                      or (not language or book['language'] != language)]

    if len(filtered_books) == len(books):
        raise HTTPException(status_code=404, detail="No matching books found")

    write_books_file(filtered_books)

    response = ResponseBook(
        status="success",
        books=filtered_books,
        count=len(filtered_books)
    )
    return JSONResponse(content=response.dict(), status_code=200)


@app.put("/books/{title}")
async def update_book_by_title(title: str, book: Book):
    return await update_book(title, book)


@app.patch("/books/{title}")
async def partial_update_book_by_title(title: str, book: Book):
    return await update_book(title, book)


async def update_book(title: str, book: Book):
    books = read_books_file()

    updated_books = []
    found = False
    for existing_book in books:
        if existing_book['title'] == title:
            updated_book = {**existing_book, **book.dict()}
            updated_books.append(updated_book)
            found = True
        else:
            updated_books.append(existing_book)

    if not found:
        raise HTTPException(status_code=404, detail="Title not found")

    write_books_file(updated_books)

    response = ResponseBook(
        status="success",
        books=updated_books,
        count=len(updated_books)
    )
    return JSONResponse(content=response.dict(), status_code=200)
