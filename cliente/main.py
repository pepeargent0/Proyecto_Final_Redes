from flask import Flask, render_template, request, redirect, session, url_for
import requests
app = Flask(__name__)
app.secret_key = 'cuantas_hamburgesas_se_comio_D$N1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

url_cliente = 'http://10.66.288.251:8000'
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
    books = requests.get(url_cliente+'/books').json()
    return render_template(
        'ingreso_vehiculos.html',
        vehiculos=books,
        ultimo_vehiculo=None,
        ultimo_sin_procesar=None,
        mensaje=None,
        user=None
    )
    return books

    print(books.text)
    print('miri')
@app.route('/salir')
def salir():
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)