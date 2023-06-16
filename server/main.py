import json
import uvicorn
import logging
from fastapi import FastAPI, HTTPException
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


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(content={"error": "HTTP exception"}, status_code=exc.status_code)


@app.get("/")
def info():
    """
    Ruta para obtener información de la versión de la API.
    """
    return JSONResponse(content={"version": "0.0.1"}, status_code=200)


@app.get("/books")
def get_books():
    """
    Ruta para obtener la lista de libros desde un archivo JSON.
    """
    file_path = "source/books.json"
    try:
        with open(file_path, "r") as file:
            json_content = file.read()
        return JSONResponse(content=json.loads(json_content), status_code=200)
    except Exception as e:
        logger.error(f"Error reading books file: {e}")
        return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)


from fastapi import Request

@app.post("/books")
def create_book(request: Request):
    """
    Ruta para crear un nuevo libro utilizando los datos proporcionados en el cuerpo de la solicitud.
    """
    try:
        book = request.json()

        # Leer la lista de libros existentes desde el archivo JSON
        file_path = "source/books.json"
        with open(file_path, "r") as file:
            books = json.load(file)

        # Agregar el nuevo libro a la lista
        books.append(book)

        # Guardar la lista actualizada de libros en el archivo JSON
        with open(file_path, "w") as file:
            json.dump(books, file, indent=4)

        return JSONResponse(content=book, status_code=201)
    except Exception as e:
        logger.error(f"Error creating book: {e}")
        return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
