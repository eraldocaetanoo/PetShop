

from flask import render_template, request, redirect, url_for, session, abort, send_file
from flask_login import login_user, login_required
from models.models import Master, Usuario
from controllers.utils.utils import tipo_usuario_requerido, login_existe, cadastrar_usuario, cadastrar_cliente, cadastrar_animal, cadastrar_tipo_servico, renderizar_lista_usuarios, gerar_relatorio, renderizar_lista_clientes
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models.models import *


# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
        with SessionLocal() as db:
            db.add(master)
            db.commit()
            # Recarrega o master da base de dados para garantir que esteja na sessão
            master = db.query(Master).filter_by(login=login).first()

            session['tipo_usuario'] = 'master'
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

@master_bp.route('/master/cadastro')
@login_required
@tipo_usuario_requerido('master')
def cadastros_realizados():
    return render_template('master/homeCadastrosRealizados.html')


@master_bp.route('/master/cadastro/usuario/list')
@login_required
@tipo_usuario_requerido('master')
def listar_usuarios():
    return renderizar_lista_usuarios()

@master_bp.route('/master/cadastro/cliente/list')
@login_required
@tipo_usuario_requerido('master')
def listar_master_clientes():
    return renderizar_lista_clientes()

@master_bp.route('/master/usuarios/editar/<tipo>/<int:id>', methods=['POST'])
@login_required
@tipo_usuario_requerido('master')
def editar_usuario(tipo,id):
    with SessionLocal() as db:
        if tipo == 'usuario':
            usuario = db.get(Usuario, id)
            if not usuario:
                abort(404)

            usuario.nome = request.form['nome']
            usuario.email = request.form['email']
            usuario.telefone = request.form['telefone']
            db.commit()
        elif tipo == 'cliente':
            cliente = db.get(Cliente, id)
            if not cliente:
                abort(404)

            cliente.nome = request.form['nome']
            cliente.email = request.form['email']
            cliente.telefone = request.form['telefone']
            db.commit()
    return redirect(url_for('master_bp.listar_usuarios'))

@master_bp.route('/master/usuarios/excluir/<int:id>', methods=['POST'])
@login_required
@tipo_usuario_requerido('master')
def excluir_usuario(id):
    with SessionLocal() as db:
        usuario = db.get(Usuario, id)
        if not usuario:
            abort(404)

        db.delete(usuario)
        db.commit()

    return redirect(url_for('master_bp.listar_usuarios'))


@master_bp.route('/master/cadastro/<tipo>/list/relatorio/pdf') #O tipo vem do template listar_usuarios.html
@login_required
@tipo_usuario_requerido('master')
def relatorio_pdf(tipo):
    pdf_file, nome_arquivo = gerar_relatorio(tipo)
    if not pdf_file:
        return "Erro ao gerar PDF", 400
    return send_file(pdf_file, download_name=nome_arquivo, as_attachment=False)




