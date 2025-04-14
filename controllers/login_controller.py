
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, login_required, logout_user
from extensions import login_manager
from models.models import Master, Usuario



login_bp = Blueprint('login_bp', __name__, template_folder='templates')




@login_bp.route('/', methods=['GET', 'POST'])
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
            return redirect(url_for('master_bp.master'))

        usuario = Usuario.query.filter_by(login=login).first()
        if usuario and usuario.senha == senha:
            login_user(usuario)
            session['tipo_usuario'] = 'usuario'
            return redirect(url_for('usuario_bp.usuario'))

        # Pode repetir o mesmo padrão para Cliente, Veterinario, etc.
        # cliente = Cliente.query.filter_by(login=login).first()
        # ...

        return "Login ou senha inválidos"


@login_manager.user_loader
def user_loader(user_id):
    tipo = session.get('tipo_usuario')

    if tipo == 'master':
        return Master.query.get(int(user_id))
    elif tipo == 'usuario':
        return Usuario.query.get(int(user_id))
    # elif tipo == 'cliente':
    #     return Cliente.query.get(int(user_id))

    return None


#faltam os outros


@login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.clear()  # Limpa o tipo do usuário e dados de sessão
    return redirect(url_for('login_bp.login'))



