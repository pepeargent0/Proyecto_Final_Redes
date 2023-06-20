import json
import logging
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import BaseModel, root_validator

app = FastAPI()
logger = logging.getLogger(__name__)


class Book(BaseModel):
    """
    Modelo de datos para representar un libro.
    """
    author: str
    country: str
    imageLink: str
    language: str
    link: str
    pages: int
    title: str
    year: int

    @root_validator
    def validate_fields(cls, values):
        """
        Validación de campos requeridos para el modelo de libro.
        """
        if not all(values.get(field) for field in cls.__fields__):
            raise ValueError("Todos los campos son requeridos")
        return values


class ResponseBook(BaseModel):
    """
    Modelo de datos para la respuesta de la API de libros.
    """
    status: str
    books: list | dict
    count: int


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    """
    Manejador de excepciones para la API.
    """
    error_message = f"Error inesperado: {exc}"
    logger.error(error_message)
    raise HTTPException(status_code=500, detail=error_message)


def read_books_file():
    """
    Lee el archivo JSON de libros y devuelve la lista de libros.
    """
    file_path = "source/books.json"
    try:
        with open(file_path, "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        error_message = f"Archivo de libros no encontrado: {file_path}"
        logger.error(error_message)
        raise HTTPException(status_code=404, detail=error_message)
    except IOError as e:
        error_message = f"Error de E/S al leer el archivo de libros: {e}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        error_message = f"Error inesperado al leer el archivo de libros: {e}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)

    return books


def write_books_file(books):
    """
    Escribe la lista de libros en el archivo JSON.
    """
    file_path = "source/books.json"
    try:
        with open(file_path, "w") as file:
            json.dump(books, file, indent=4)
    except IOError as e:
        error_message = f"Error de E/S al escribir en el archivo de libros: {e}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        error_message = f"Error inesperado al escribir en el archivo de libros: {e}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)


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

    Parámetros:
    - country (str): País del autor del libro.
    - language (str): Idioma del libro.
    - author (str): Autor del libro.
    - year (int): Año de publicación del libro.

    Respuesta:
    - status (str): Estado de la respuesta ("success").
    - books (list | dict): Lista de libros filtrados por los parámetros proporcionados.
    - count (int): Cantidad de libros encontrados.
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
    """
    Ruta para crear un nuevo libro.

    Parámetros:
    - book (Book): Objeto que representa el libro a crear.

    Respuesta:
    - status (str): Estado de la respuesta ("success").
    - books (dict): Datos del libro creado.
    - count (int): Cantidad de libros creados (siempre será 1).
    """
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
    """
    Ruta para eliminar libros según los parámetros proporcionados.

    Parámetros (opcionales):
    - author (str): Autor del libro a eliminar.
    - year (int): Año de publicación del libro a eliminar.
    - country (str): País del autor del libro a eliminar.
    - title (str): Título del libro a eliminar.
    - language (str): Idioma del libro a eliminar.

    Si no se proporcionan parámetros, se eliminarán todos los libros.

    Respuesta:
    - status (str): Estado de la respuesta ("success").
    - books (list): Lista de libros después de eliminar los libros coincidentes.
    - count (int): Cantidad de libros restantes después de la eliminación.
    """
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
@app.patch("/books/{title}")
async def update_book_by_title(title: str, book: Book):
    """
    Ruta para actualizar un libro según el título.

    Parámetros:
    - title (str): Título del libro a actualizar.
    - book (Book): Objeto que representa los datos actualizados o parcialmente actualizados del libro.

    Respuesta:
    - status (str): Estado de la respuesta ("success").
    - books (list): Lista de libros después de la actualización.
    - count (int): Cantidad de libros después de la actualización.
    """
    books = read_books_file()

    updated_books = []
    found = False

    for existing_book in books:
        if existing_book['title'] == title:
            found = True
            updated_book = {**existing_book, **book.dict()}
            updated_books.append(updated_book)
        else:
            updated_books.append(existing_book)

    if not found:
        raise HTTPException(status_code=404, detail=f"Book with title '{title}' not found")

    write_books_file(updated_books)

    response = ResponseBook(
        status="success",
        books=updated_books,
        count=len(updated_books)
    )
    return JSONResponse(content=response.dict(), status_code=200)
