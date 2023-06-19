import requests

# URL base del servidor FastAPI
base_url = "http://localhost:8000"


# Obtener información de la versión de la API
def get_api_version():
    url = f"{base_url}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        version = data.get("version")
        print(f"Versión de la API: {version}")
    else:
        print("Error al obtener la versión de la API")


# Obtener la lista de libros filtrada
def get_filtered_books(params):
    url = f"{base_url}/books"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        books = data.get("books")
        count = data.get("count")
        print(f"Total de libros encontrados: {count}")
        for book in books:
            print("-----")
            print(f"Autor: {book['author']}")
            print(f"Título: {book['title']}")
            # Agrega más campos según tus necesidades
    else:
        print("Error al obtener la lista de libros")


# Crear un nuevo libro
def create_book(book_data):
    url = f"{base_url}/books"
    response = requests.post(url, json=book_data)
    if response.status_code == 201:
        data = response.json()
        book = data.get("books")
        print("Libro creado exitosamente:")
        print(f"Autor: {book['author']}")
        print(f"Título: {book['title']}")
        # Agrega más campos según tus necesidades
    else:
        print("Error al crear el libro")


# Eliminar libros filtrados
def delete_filtered_books(params):
    url = f"{base_url}/books"
    response = requests.delete(url, params=params)
    if response.status_code == 200:
        data = response.json()
        count = data.get("count")
        print(f"Total de libros eliminados: {count}")
    else:
        print("Error al eliminar los libros")


# Actualizar un libro por título
def update_book_by_title(title, book_data):
    url = f"{base_url}/books/{title}"
    response = requests.put(url, json=book_data)
    if response.status_code == 200:
        data = response.json()
        books = data.get("books")
        count = data.get("count")
        print(f"Total de libros actualizados: {count}")
        for book in books:
            print("-----")
            print(f"Autor: {book['author']}")
            print(f"Título: {book['title']}")
            # Agrega más campos según tus necesidades
    else:
        print("Error al actualizar el libro")


# Obtener información de la versión de la API
get_api_version()

# Filtrar libros por autor y año
params = {
    "author": "Autor Ejemplo",
    "year": 2022
}
get_filtered_books(params)

# Crear un nuevo libro
new_book = {
    "author": "Nuevo Autor",
    "title": "Nuevo Libro",
    # Agrega más campos según los definidos en el modelo Book
}
create_book(new_book)

# Eliminar libros por país
params = {
    "country": "País Ejemplo"
}
delete_filtered_books(params)

# Actualizar un libro por título
title = "Título Ejemplo"
updated_book = {
    "author": "Autor Actualizado"
}
update_book_by_title(title, updated_book)
