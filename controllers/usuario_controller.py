

from flask import render_template, send_file
from flask_login import login_required
from models.models import *
# from .login_controller import *
from controllers.utils.utils import tipo_usuario_requerido, cadastrar_cliente, cadastrar_animal, cadastrar_tipo_servico, gerar_relatorio, renderizar_lista_clientes
from flask import Blueprint


# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/usuario')


@usuario_bp.route('/home')
@login_required
@tipo_usuario_requerido('usuario')
def usuario():
    return render_template('usuario/homeUsuario.html')

@usuario_bp.route('/cadastro')
@login_required
@tipo_usuario_requerido('usuario')
def cadastros_realizados():
    return render_template('usuario/homeCadastrosRealizados.html')

@usuario_bp.route('/cadastro/cliente/list')
@login_required
@tipo_usuario_requerido('usuario')
def listar_usuario_clientes():
    return renderizar_lista_clientes()


@usuario_bp.route('/cadastro/cliente', methods=['GET', 'POST'])
@login_required
@tipo_usuario_requerido('usuario')
def cadastro_cliente():
    return cadastrar_cliente('usuario')


@usuario_bp.route('/cadastro/animal', methods=['GET', 'POST'])
@login_required
@tipo_usuario_requerido('usuario')
def cadastro_animal():
    return cadastrar_animal('usuario')

@usuario_bp.route('/cadastro/tipo-servico', methods=['GET', 'POST'])
@login_required
@tipo_usuario_requerido('usuario')
def cadastro_tipo_servico():
    return cadastrar_tipo_servico('usuario')


@usuario_bp.route('/<tipo>/list/relatorio/pdf') #O tipo vem do template listar_usuarios.html
@login_required
@tipo_usuario_requerido('usuario')
def relatorio_pdf(tipo):
    pdf_file, nome_arquivo = gerar_relatorio(tipo)
    if not pdf_file:
        return "Erro ao gerar PDF", 400
    return send_file(pdf_file, download_name=nome_arquivo, as_attachment=False)
