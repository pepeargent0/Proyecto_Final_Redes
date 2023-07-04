import logging
from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
app.secret_key = 'cuantas_hamburguesas_se_comio_D$N1'

url_server = 'http://localhost:8000'

# Configurar el registro de eventos
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Renderiza la página de inicio de sesión y gestiona la autenticación del usuario.

    Si el usuario proporciona credenciales válidas, se redirige a la página '/books'.
    De lo contrario, se muestra un mensaje de error en la página de inicio de sesión.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            return redirect('/books')
        else:
            error_message = 'Credenciales inválidas.'
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')


@app.route('/books', methods=['GET'])
def books():
    """
    Obtiene la lista de libros desde el servicio externo y renderiza la plantilla 'books.html'.

    Si ocurre un error al obtener los libros, se muestra un mensaje de error.
    """
    try:
        response = requests.get(url_server + '/books')
        response.raise_for_status()
        books = response.json().get('books', [])
        return render_template('books.html', books=books, user=None)
    except requests.exceptions.RequestException as e:
        error_message = 'Error al obtener los libros: {}'.format(e)
        logger.error(error_message)
        return render_template('error.html', error_message=error_message)


@app.route('/books/borrar/<string:title>', methods=['GET'])
def delete(title):
    """
    Elimina un libro con el título especificado desde el servicio externo.

    Después de eliminar el libro, se redirige al usuario a la página '/books'.

    Si ocurre un error durante el proceso de eliminación, se muestra un mensaje de error.
    """
    try:
        response = requests.delete(url_server + '/books', params={'title': title})
        response.raise_for_status()
        return redirect('/books')
    except requests.exceptions.RequestException as e:
        error_message = 'Error al borrar el libro: {}'.format(e)
        logger.error(error_message)
        return render_template('error.html', error_message=error_message)


@app.route('/books/crear', methods=['POST', 'GET'])
def create():
    """
    Crea un nuevo libro enviando una solicitud POST al servicio externo.

    Si la creación del libro es exitosa, se redirige al usuario a la página '/books'.
    Si ocurre un error durante el proceso de creación, se muestra un mensaje de error.
    """
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            response = requests.post(url_server + '/books', json=data)
            response.raise_for_status()
            return redirect('/books')
        except requests.exceptions.RequestException as e:
            error_message = 'Error al crear el libro: {}'.format(e)
            logger.error(error_message)
            return render_template('error.html', error_message=error_message)
    else:
        return render_template('edit_books.html', book=None, user=None)


@app.route('/books/editar/<string:title>', methods=['POST', 'GET'])
def editar(title):
    """
    Edita un libro con el título especificado enviando una solicitud PUT al servicio externo.

    Si la edición del libro es exitosa, se redirige al usuario a la página '/books'.
    Si ocurre un error durante el proceso de edición, se muestra un mensaje de error.
    """
    if request.method == 'POST':
        try:
            updated_book_data = dict(request.form)
            response = requests.put(url_server + '/books/' + title, json=updated_book_data)
            response.raise_for_status()
            return redirect('/books')
        except requests.exceptions.RequestException as e:
            error_message = 'Error al editar el libro: {}'.format(e)
            logger.error(error_message)
            return render_template('error.html', error_message=error_message)
    else:
        try:
            response = requests.get(url_server + '/books', params={'title': title})
            response.raise_for_status()
            book_details = response.json().get('books', [])[0]
            return render_template('edit_books.html', book=book_details, user=None)
        except requests.exceptions.RequestException as e:
            error_message = 'Error al obtener los detalles del libro: {}'.format(e)
            logger.error(error_message)
            return render_template('error.html', error_message=error_message)


@app.route('/salir')
def salir():
    """
    Redirige al usuario a la URL principal ('/') cuando elige cerrar sesión.
    """
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
