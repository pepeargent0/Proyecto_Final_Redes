import requests


def descargar_archivo(url, ruta_guardado):
    response = requests.get(url)
    if response.status_code == 200:
        with open(ruta_guardado, 'wb') as archivo:
            archivo.write(response.content)
        print("Archivo descargado correctamente.")
    else:
        print("Error al descargar el archivo.")


# URL del archivo JSON
url = "https://raw.githubusercontent.com/benoitvallon/100-best-books/master/books.json"

# Ruta donde deseas guardar el archivo
ruta_guardado = "source/books.json"

# Llamada a la función para descargar el archivo
descargar_archivo(url, ruta_guardado)
