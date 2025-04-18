

from flask import render_template
from flask_login import login_required

# from .login_controller import *
from controllers.utils.utils import tipo_usuario_requerido, cadastrar_cliente, cadastrar_animal, cadastrar_tipo_servico
from flask import Blueprint


usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/usuario')


@usuario_bp.route('/home')
@login_required
@tipo_usuario_requerido('usuario')
def usuario():
    return render_template('usuario/homeUsuario.html')


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