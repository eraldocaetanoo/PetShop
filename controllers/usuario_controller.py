from main import app
from functools import wraps
from flask import render_template, request, redirect, url_for, session, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.models import *

lm = LoginManager(app)


def tipo_usuario_requerido(tipo):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if session.get('tipo_usuario') != tipo:
                abort(403)  # Proibido
            return func(*args, **kwargs)
        return decorated_view
    return wrapper



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        # Tenta encontrar em cada tipo de usuário
        master = Master.query.filter_by(login=login).first()
        if master and master.senha == senha:
            login_user(master)
            session['tipo_usuario'] = 'master'
            return redirect(url_for('master'))

        usuario = Usuario.query.filter_by(login=login).first()
        if usuario and usuario.senha == senha:
            login_user(usuario)
            session['tipo_usuario'] = 'usuario'
            return redirect(url_for('usuario'))

        # Pode repetir o mesmo padrão para Cliente, Veterinario, etc.
        # cliente = Cliente.query.filter_by(login=login).first()
        # ...

        return "Login ou senha inválidos"


@lm.user_loader
def user_loader(user_id):
    tipo = session.get('tipo_usuario')

    if tipo == 'master':
        return Master.query.get(int(user_id))
    elif tipo == 'usuario':
        return Usuario.query.get(int(user_id))
    # elif tipo == 'cliente':
    #     return Cliente.query.get(int(user_id))

    return None

    


# Cadastro do Master (Se for só um master, só se faz isso uma vez)
@app.route('/cadastro/master', methods = ['GET','POST'])
@tipo_usuario_requerido('master') # PARA CADASTRAR MASTER TEM QUE REMOVER ESSA LINHA
def cadastrarmaster():
    if request.method == 'GET':
        return render_template('/cadastroMaster.html')
    elif request.method =='POST':
        nome = request.form['masterNome']
        login = request.form['masterLogin']
        senha = request.form['masterSenha']

        master = Master(nome=nome, login=login, senha=senha)
        db.session.add(master)
        db.session.commit()

        session['tipo_usuario'] = 'master'  # <-- Isso aqui ANTES do login_user
        login_user(master)

        return redirect(url_for('master'))
        

@app.route('/master/cadastro/usuario', methods = ['GET','POST'])
@login_required
@tipo_usuario_requerido('master')
def cadastro_usuario():
    if request.method == 'GET':
        return render_template('/master/cadastroUsuario.html')
    elif request.method =='POST':
        nome = request.form['usuarioNome']
        login = request.form['usuarioLogin']
        senha = request.form['usuarioSenha']
        email = request.form['usuarioEmail']
        telefone = request.form['usuarioTelefone']

        if login_existe(login):
            return render_template('/master/cadastroUsuario.html', erro="Esse login já está em uso. Escolha outro.")

        usuario = Usuario(nome=nome, login=login, senha=senha, email=email, telefone=telefone)
        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for('cadastro_usuario'))


@app.route('/master/home')
@login_required
@tipo_usuario_requerido('master')
def master():
    return render_template('master/home.html')



@app.route('/usuario/home')
@login_required
@tipo_usuario_requerido('usuario')
def usuario():
    return render_template('usuario/home.html')




#faltam os outros


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.clear()  # Limpa o tipo do usuário e dados de sessão
    return redirect(url_for('login'))


def login_existe(login):
    if Master.query.filter_by(login=login).first():
        return True
    if Usuario.query.filter_by(login=login).first():
        return True
    
    return False
