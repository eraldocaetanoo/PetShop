

from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, login_required
from models.models import db, Master, Usuario
from controllers.utils.utils import tipo_usuario_requerido, login_existe, cadastrar_usuario, cadastrar_cliente, cadastrar_animal, cadastrar_tipo_servico
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash




master_bp = Blueprint('master_bp', __name__)


# Cadastro do Master (Se for só um master, só se faz isso uma vez)
@master_bp.route('/cadastro/master', methods = ['GET','POST'])
#@tipo_usuario_requerido('master') # PARA CADASTRAR MASTER TEM QUE REMOVER ESSA LINHA
def cadastrarmaster():
    if request.method == 'GET':
        return render_template('/cadastroMaster.html')
    elif request.method =='POST':
        nome = request.form['masterNome']
        login = request.form['masterLogin']
        senha = request.form['masterSenha']
        senha_hash = generate_password_hash(senha)  # senha é o valor vindo do form
        
        if login_existe(login):
            return render_template('/cadastroMaster.html', erro="Esse login já está em uso. Escolha outro.")


        master = Master(nome=nome, login=login, senha=senha_hash)
        db.session.add(master)
        db.session.commit()

        session['tipo_usuario'] = 'master'  # <-- Isso aqui ANTES do login_user
        login_user(master)

        return redirect(url_for('master_bp.master'))

@master_bp.route('/master/cadastro/usuario', methods=['GET', 'POST'])
@login_required
@tipo_usuario_requerido('master')
def cadastro_usuario():
    return cadastrar_usuario('master')

@master_bp.route('/master/cadastro/cliente', methods=['GET', 'POST'])
@login_required
@tipo_usuario_requerido('master')
def cadastro_cliente():
    return cadastrar_cliente('master')

@master_bp.route('/master/cadastro/animal', methods=['GET', 'POST'])
@login_required
@tipo_usuario_requerido('master')
def cadastro_animal():
    return cadastrar_animal('master')

@master_bp.route('/master/cadastro/tipo-servico', methods=['GET', 'POST'])
@login_required
@tipo_usuario_requerido('master')
def cadastro_tipo_servico():
    return cadastrar_tipo_servico('master')


@master_bp.route('/master/home')
@login_required
@tipo_usuario_requerido('master')
def master():
    return render_template('master/homeMaster.html')


# @master_bp.route('/master/cadastro/usuario', methods = ['GET','POST'])
# @login_required
# @tipo_usuario_requerido('master')
# def cadastro_usuario():
#     if request.method == 'GET':
#         return render_template('/usuario/cadastroUsuario.html')
#     elif request.method =='POST':
#         nome = request.form['usuarioNome']
#         login = request.form['usuarioLogin']
#         senha = request.form['usuarioSenha']
#         senha_hash = generate_password_hash(senha)  # senha é o valor vindo do form
#         email = request.form['usuarioEmail']
#         telefone = request.form['usuarioTelefone']

#         if login_existe(login):
#             return render_template('/usuario/cadastroUsuario.html')

#         usuario = Usuario(nome=nome, login=login, senha=senha_hash, email=email, telefone=telefone)
#         db.session.add(usuario)
#         db.session.commit()

#         return redirect(url_for('master_bp.cadastro_usuario'))


