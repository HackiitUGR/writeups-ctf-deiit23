#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for, send_file, abort
import random
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flag')
def serve_flag():
    if request.remote_addr != '127.0.0.1':
        abort(403)
    else:
        return send_file('./flag', mimetype='text/plain')

@app.route('/process', methods=['POST'])
def process():
    url = request.form['url']

    # Validamos la URL ingresada por el usuario.
    if '.jpg' not in url:
        return 'No es una imagen JPG'

    # Restringimos el acceso a la dirección localhost.
    if 'localhost' in url or '127.0.0.' in url:
        return 'No se permite acceder a la dirección localhost'

    # Generamos nombre random para el fichero
    filename = ''
    for _ in range(10):
        filename += chr(random.randint(97, 122))
        filename += chr(random.randint(65, 90))

    # Descargamos la imagen utilizando requests.
    r = requests.get(url, allow_redirects=True)
    open('./static/' + filename, 'wb').write(r.content)

    # Devolvemos el mensaje de éxito al usuario.
    return redirect(url_for('display', filename=filename))

@app.route('/display/<filename>')
def display(filename):
    if filename:
        return render_template('display.html', filename=filename)
    else:
        return 'Error al cargar la imagen.'

if __name__ == '__main__':
    app.run(debug=False,port=5002, static_url_path='/static')
