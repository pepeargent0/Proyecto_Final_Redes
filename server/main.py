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

    @validator('author', 'country', 'imageLink', 'language', 'link', 'pages', 'title', 'year')
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
    file_path = "source/books.json"
    try:
        with open(file_path, "r") as file:
            books = json.load(file)
        if author:
            books = [book for book in books if book['author'] == author]
        if language:
            books = [book for book in books if book['language'] == language]
        if year:
            books = [book for book in books if book['year'] == year]
        if country:
            books = [book for book in books if book['country'] == country]
        response = ResponseBook(
            status="success",
            books=books,
            count=len(books)
        )
        return JSONResponse(content=response.dict(), status_code=200)
    except Exception as e:
        logger.error(f"Error reading books file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/books")
async def create_book(book: Book):
    file_path = "source/books.json"
    try:
        with open(file_path, "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        books = []
    books.append(book.dict())
    try:
        with open(file_path, "w") as file:
            json.dump(books, file, indent=4)
        response = ResponseBook(
            status="success",
            books=book.dict(),
            count=1
        )
        return JSONResponse(content=response.dict(), status_code=201)
    except Exception as e:
        logger.error(f"Error creating book: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete("/books")
async def delete_book(author: str = None, year: int = None, country: str = None):
    file_path = "source/books.json"
    try:
        with open(file_path, "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Books file not found")

    filtered_books = books.copy()

    if author:
        filtered_books = [book for book in filtered_books if book['author'] != author]
    if year:
        filtered_books = [book for book in filtered_books if book['year'] != year]
    if country:
        filtered_books = [book for book in filtered_books if book['country'] != country]

    if len(filtered_books) == len(books):
        raise HTTPException(status_code=404, detail="No matching books found")

    try:
        with open(file_path, "w") as file:
            json.dump(filtered_books, file, indent=4)
        response = ResponseBook(
            status="success",
            books=filtered_books,
            count=len(filtered_books)
        )
        return JSONResponse(content=response.dict(), status_code=200)
    except Exception as e:
        logger.error(f"Error deleting book(s): {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.put("/books/{author}")
async def update_book(author: str, book: Book):
    file_path = "source/books.json"
    try:
        with open(file_path, "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Books file not found")
    updated_books = []
    found = False
    for existing_book in books:
        if existing_book['author'] == author:
            updated_books.append(book.dict())
            found = True
        else:
            updated_books.append(existing_book)
    if not found:
        raise HTTPException(status_code=404, detail="Author not found")
    try:
        with open(file_path, "w") as file:
            json.dump(updated_books, file, indent=4)
        response = ResponseBook(
            status="success",
            books=updated_books,
            count=len(updated_books)
        )
        return JSONResponse(content=response.dict(), status_code=200)
    except Exception as e:
        logger.error(f"Error updating book: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.patch("/books/{author}")
async def partial_update_book(author: str, book: Book):
    file_path = "source/books.json"
    try:
        with open(file_path, "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Books file not found")
    updated_books = []
    found = False
    for existing_book in books:
        if existing_book['author'] == author:
            updated_book = {**existing_book, **book.dict()}
            updated_books.append(updated_book)
            found = True
        else:
            updated_books.append(existing_book)
    if not found:
        raise HTTPException(status_code=404, detail="Author not found")
    try:
        with open(file_path, "w") as file:
            json.dump(updated_books, file, indent=4)
        response = ResponseBook(
            status="success",
            books=updated_books,
            count=len(updated_books)
        )
        return JSONResponse(content=response.dict(), status_code=200)
    except Exception as e:
        logger.error(f"Error updating book: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
