from main import app
from flask import render_template, request, redirect, url_for, session, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.models import *

lm = LoginManager(app)

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

        session['tipo_usuario'] = 'master'  # <-- Isso aqui ANTES do login_use
        login_user(master)
        return redirect(url_for('master'))
        

@app.route('/master/cadastro_usuario', methods = ['GET','POST'])
def cadastro_usuario():
    if request.method == 'GET':
        return render_template('/master/cadastroUsuario.html')
    elif request.method =='POST':
        nome = request.form['usuarioNome']
        login = request.form['usuarioLogin']
        senha = request.form['usuarioSenha']
        email = request.form['usuarioEmail']
        telefone = request.form['usuarioTelefone']

        usuario = Usuario(nome=nome, login=login, senha=senha, email=email, telefone=telefone)
        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for('cadastro_usuario'))


@app.route('/master')
@login_required
def master():
    if session.get('tipo_usuario') != 'master':
        abort(403)  # Erro "Proibido"
    return render_template('master/home.html')

@app.route('/usuario')
@login_required
def usuario():
    if session.get('tipo_usuario') != 'usuario':
        abort(403)  # Erro "Proibido"
    return render_template('usuario/home.html')



#faltam os outros


@app.route('/logout')
def logout():
    logout_user()
    session.clear()  # Limpa o tipo do usuário e dados de sessão
    return redirect(url_for('login'))
