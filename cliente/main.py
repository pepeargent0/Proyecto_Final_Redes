import requests

# URL base de la API
base_url = "http://localhost:8000"

# Obtener información de la versión de la API
def get_api_version():
    url = base_url + "/"
    response = requests.get(url)
    data = response.json()
    return data["version"]

# Obtener la lista de libros
def get_books():
    url = base_url + "/books"
    response = requests.get(url)
    data = response.json()
    return data["books"]

# Obtener la lista de libros por autor
def get_books_by_author(author):
    url = base_url + f"/books/{author}"
    response = requests.get(url)
    data = response.json()
    return data["books"]

# Crear un nuevo libro
def create_book(book_data):
    url = base_url + "/books"
    response = requests.post(url, json=book_data)
    data = response.json()
    return data["books"]

# Ejemplo de uso
if __name__ == "__main__":
    # Obtener información de la versión de la API
    version = get_api_version()
    print("API Version:", version)

    # Obtener la lista de libros
    books = get_books()
    print("Books:")
    for book in books:
        print(book)


    # Obtener la lista de libros por autor
    author = "John Doe"
    books_by_author = get_books_by_author(author)
    print(f"Books by {author}:")
    for book in books_by_author:
        print(book)

    # Crear un nuevo libro
    new_book_data = {
        "author": "Jane Smith",
        "country": "United States",
        "imageLink": "https://example.com/book.jpg",
        "language": "English",
        "link": "https://example.com/book",
        "pages": 200,
        "title": "New Book",
        "year": 2022
    }
    created_book = create_book(new_book_data)
    print("Created Book:", created_book)
