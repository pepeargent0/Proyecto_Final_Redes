import json

import uvicorn
import logging
from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi.exceptions import HTTPException as FastAPIHTTPException

app = FastAPI()
logger = logging.getLogger(__name__)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(content={"error": "Validation error"}, status_code=400)


@app.exception_handler(FastAPIHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(content={"error": "HTTP exception"}, status_code=exc.status_code)


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
