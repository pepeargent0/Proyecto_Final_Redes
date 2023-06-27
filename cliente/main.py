import requests

# URL base del servidor
base_url = "http://localhost:8000"

def get_books(params=None):
    """
    Obtiene la lista de libros desde el servidor.

    Parámetros:
    - params (dict): Parámetros de filtrado de libros (opcional).

    Retorna:
    - data (dict): Datos de respuesta del servidor.
    """
    url = f"{base_url}/books"
    response = requests.get(url, params=params)
    response.raise_for_status()  # Verificar si se produjo un error en la respuesta
    data = response.json()
    return data

def create_book(book_data):
    """
    Crea un nuevo libro en el servidor.

    Parámetros:
    - book_data (dict): Datos del libro a crear.

    Retorna:
    - data (dict): Datos de respuesta del servidor.
    """
    url = f"{base_url}/books"
    response = requests.post(url, json=book_data)
    response.raise_for_status()  # Verificar si se produjo un error en la respuesta
    data = response.json()
    return data

def delete_books(params=None):
    """
    Elimina libros del servidor según los parámetros proporcionados.

    Parámetros (opcionales):
    - params (dict): Parámetros de filtrado de libros a eliminar.

    Retorna:
    - data (dict): Datos de respuesta del servidor.
    """
    url = f"{base_url}/books"
    response = requests.delete(url, params=params)
    response.raise_for_status()  # Verificar si se produjo un error en la respuesta
    data = response.json()
    return data

def update_book_by_title(title, book_data):
    """
    Actualiza un libro en el servidor según el título.

    Parámetros:
    - title (str): Título del libro a actualizar.
    - book_data (dict): Datos actualizados del libro.
    Retorna:
    - data (dict): Datos de respuesta del servidor.
    """
    url = f"{base_url}/books/{title}"
    response = requests.put(url, json=book_data)
    response.raise_for_status()  # Verificar si se produjo un error en la respuesta
    data = response.json()
    return data
# Ejemplos de uso
try:
    # Obtener la lista de todos los libros
    books_data = get_books()
    print("Lista de libros:")
    for book in books_data['books']:
        print(book)
    # Filtrar libros por autor
    params = {'author': 'John Doe'}
    filtered_books_data = get_books(params)
    print("Lista de libros filtrados por autor:")
    for book in filtered_books_data['books']:
        print(book)
    # Crear un nuevo libro
    new_book_data = {
        "author": "Jane Smith",
        "country": "United States",
        "imageLink": "example.com/image.jpg",
        "language": "English",
        "link": "example.com/book",
        "pages": 200,
        "title": "New Book",
        "year": 2022
    }
    created_book_data = create_book(new_book_data)
    print("Libro creado:")
    print(created_book_data['books'])
    # Eliminar libros por año
    delete_params = {'year': 2020}
    deleted_books_data = delete_books(delete_params)
    print(deleted_books_data)
    print(f"Libros eliminados: {deleted_books_data['count']}")
    # Actualizar un libro por título
    update_book_data = {
        "author": "Jane Smith",
        "year": 2023
    }
    updated_book_data = update_book_by_title("New Book", update_book_data)
    print("Libro actualizado:")
    print(updated_book_data['books'])
except requests.exceptions.HTTPError as e:
    print(f"Error en la solicitud HTTP: {e}")
except requests.exceptions.RequestException as e:
    print(f"Error al realizar la solicitud: {e}")
except KeyError as e:
    print(f"Error de clave: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
