from flask import Flask, render_template, request, redirect, session, url_for
import requests

app = Flask(__name__)
app.secret_key = 'cuantas_hamburgesas_se_comio_D$N1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

url_cliente = 'http://localhost:8000'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            return redirect('/books')
        else:
            error_message = 'Credenciales inválidas.'
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')


@app.route('/books', methods=['GET', 'POST'])
def books():
    books = requests.get(url_cliente + '/books').json()
    return render_template(
        'books.html',
        books=books['books'],
        user=None
    )



@app.route('/books/borrar/<string:title>',  methods=['GET'])
def delete(title):
    params = {'title': title}
    response = requests.delete(url_cliente + '/books', params=params)
    if response.status_code == 200:
        return redirect('/books')
    else:
        # Mostrar el mensaje de error en caso de fallo
        print("Error:", response.text)
    print(title)


@app.route('/books/crear', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        data = request.form.to_dict()
        create_book = requests.post(url_cliente + '/books', params=data)
        print(create_book.status_code)
        print(request.form)
    else:
        return render_template(
            'edit_books.html',
            book=None,
            user=None
        )


@app.route('/books/editar/<string:title>', methods=['POST', 'GET'])
def editar(title):
    if request.method == 'POST':
        updated_book_data = dict(request.form)
        response = requests.put(url_cliente + '/books/'+title, json=updated_book_data)
        if response.status_code == 200:
            return redirect('/books')
        else:
            # Mostrar el mensaje de error en caso de fallo
            print("Error:", response.text)
    else:
        book = requests.get(url_cliente + '/books?title='+title).json()
        book_details = book['books'][0]
        return render_template(
            'edit_books.html',
            book=book_details,
            user=None
        )


@app.route('/salir')
def salir():
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
