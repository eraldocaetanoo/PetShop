from main import app
from flask import render_template



# Definição de uma rota
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/homepage')
def homepage():
    return "sss"

@app.route('/master')
def master():
    return "Master"

@app.route('/cadastro_usuario')
def cadastro_usuario():
    return render_template('usuario/cadastro.html')