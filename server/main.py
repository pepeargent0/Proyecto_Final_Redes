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
async def get_books():
    """
    Ruta para obtener la lista de libros desde un archivo JSON.
    """
    file_path = "source/books.json"
    try:
        with open(file_path, "r") as file:
            books = json.load(file)
        response = ResponseBook(
            status="success",
            books=books,
            count=len(books)
        )
        return JSONResponse(content=response.dict(), status_code=200)
    except Exception as e:
        logger.error(f"Error reading books file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/books/{author}")
async def get_author_books(author: str):
    """
    Ruta para obtener la lista de libros desde un archivo JSON.
    """
    file_path = "source/books.json"
    try:
        with open(file_path, "r") as file:
            books = json.load(file)
        """
        mirian esto es lo mismo pero me gusta mas en 1 renglon
        books_author = []
        for book in books:
            if book['author'] == author:
                books_author.append(book)
        """
        books_author = [book for book in books if book['author'] == author]
        response = ResponseBook(
            status="success",
            books=books_author,
            count=len(books_author)
        )
        return JSONResponse(content=response.dict(), status_code=200)
    except Exception as e:
        logger.error(f"Error reading books file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# TODO
"""
agregar filtro por country es una ruta
agregar filtro por language 
agregar filtro por año so 3 rutas :)
Falta AGREGAR DELETE, PUT y PATCH
CUANDO TERMINES filtro, country, y año revisar si hay codigo repetido :(
"""


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
