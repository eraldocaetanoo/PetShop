

from flask import render_template
from flask_login import login_required

# from .login_controller import *
from extensions import tipo_usuario_requerido

from flask import Blueprint

usuario_bp = Blueprint('usuario_bp', __name__)


@usuario_bp.route('/usuario/home')
@login_required
@tipo_usuario_requerido('usuario')
def usuario():
    return render_template('usuario/homeUsuario.html')