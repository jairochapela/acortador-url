import random
import secrets
from flask import Flask, abort, render_template, request, redirect, url_for, flash
from model import LETRAS, Ruta
import os
import re
from markupsafe import Markup, escape


app = Flask(__name__)


APP_BASE_URL =  os.environ.get('APP_BASE_URL', 'http://127.0.0.1:5000')
CODE_SIZE = int(os.environ.get('CODE_SIZE', 10))


@app.route('/', methods=['GET', 'POST'])
def crear_ruta():
    with app.app_context():
        if request.method == 'POST':
            if not request.form['url']:
                flash('Falta el URL')
                return redirect(url_for('crear_url'))
            codigo = "".join(random.choices(LETRAS, k=CODE_SIZE))
            ruta = Ruta(codigo, request.form['url'])
            ruta.save()
            return render_template('enlace.html', baseurl=APP_BASE_URL, ruta=ruta)
        elif request.method == 'GET':
            return render_template('crear_ruta.html')


@app.route('/<codigo>', methods=['GET'])
def ver_ruta(codigo):
    with app.app_context():
        ruta = Ruta.get(codigo)
        if ruta:
            return redirect(ruta.url_original)
        else:
            abort(404, description="Ruta no válida") 


@app.route('/w/<codigo>', methods=['GET'])
def ver_ruta_words(codigo):
    with app.app_context():
        ruta = Ruta.find_by_words(codigo)
        if ruta:
            return redirect(ruta.url_original)
        else:
            abort(404, description="Ruta no válida") 


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)


if __name__ == '__main__':
    with app.app_context():
        Ruta.create_db()

    app.run(debug=True)

