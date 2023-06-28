from flask import Flask, render_template, request, redirect, session, url_for
import requests

app = Flask(__name__)
app.secret_key = 'cuantas_hamburgesas_se_comio_D$N1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

url_cliente = 'http://10.66.228.251:8000'


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


@app.route('/books/borrar/<str:title>')
def delete(title):
    print(title)


@app.route('/books/crear', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        print(request.form)
    else:
        print('retorno vista crear')


@app.route('/books/editar/<str:title>', methods=['POST', 'GET'])
def editar(title):
    if request.method == 'POST':
        print('actualiza libro')
    else:
        print('get libro')


@app.route('/salir')
def salir():
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
