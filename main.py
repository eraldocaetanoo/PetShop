from flask import Flask, render_template, request, redirect, url_for

from models.models import db, Master

import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db.init_app(app)

from controllers.usuario_controller import *


#Inicia o servidor de desenvolvimento.
if __name__ == '__main__':
    # Verifica se o arquivo do banco de dados existe
    if not os.path.exists('database.db'):
        with app.app_context():
            db.create_all() # Cria o banco de dados apenas se não existir

    app.run(debug=True)