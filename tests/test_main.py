import unittest
from fastapi.testclient import TestClient
from server.main import app, Book

client = TestClient(app)


class TestBookAPI(unittest.TestCase):
    def setUp(self):
        # Preparar datos de prueba
        self.book = Book(
            author="John Doe",
            country="United States",
            imageLink="example.com/image.jpg",
            language="English",
            link="example.com/book",
            pages=200,
            title="Test Book",
            year=2022
        )

    def tearDown(self):
        # Limpiar datos de prueba (opcional)
        pass

    def test_info(self):
        # Prueba para la ruta "/"
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"version": "0.0.1"})

    def test_create_book(self):
        # Prueba para crear un nuevo libro
        response = client.post("/books", json=self.book.dict())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["books"], self.book.dict())
        self.assertEqual(response.json()["count"], 1)

    def test_get_books(self):
        # Prueba para obtener la lista de libros
        response = client.get("/books")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertIsInstance(response.json()["books"], list)
        self.assertGreaterEqual(response.json()["count"], 0)

    def test_get_author_books(self):
        # Prueba para obtener la lista de libros de un autor específico
        response = client.get("/books/John Doe")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertIsInstance(response.json()["books"], list)
        self.assertGreaterEqual(response.json()["count"], 0)

    def test_get_nonexistent_author_books(self):
        # Prueba para obtener la lista de libros de un autor inexistente
        response = client.get("/books/Unknown Author")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertIsInstance(response.json()["books"], list)
        self.assertEqual(response.json()["count"], 0)

    def test_get_books_error(self):
        # Prueba para manejo de errores al obtener la lista de libros
        # Modifica el archivo "source/books.json" para que no se pueda leer correctamente
        response = client.get("/books")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["error"], "Internal Server Error")

    def test_create_book_error(self):
        # Prueba para manejo de errores al crear un libro
        # Modifica el archivo "source/books.json" para que no se pueda escribir correctamente
        response = client.post("/books", json=self.book.dict())
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["error"], "Internal Server Error")

"""
if __name__ == "__main__":
    unittest.main()
"""