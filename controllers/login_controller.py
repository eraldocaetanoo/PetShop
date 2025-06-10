from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, login_required, logout_user
from controllers.utils.utils import login_manager, login_existe, SessionLocal
from models.models import Master, Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import scoped_session

login_bp = Blueprint('login_bp', __name__, template_folder='templates')

# Cria sessão segura com escopo de thread (boa prática com Flask)
db_session = scoped_session(SessionLocal)


@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        login_input = request.form['login']
        senha_input = request.form['senha']

        db = SessionLocal()
        try:
            # Verifica Master
            master = db.query(Master).filter_by(login=login_input).first()
            if master and check_password_hash(master.senha, senha_input):
                login_user(master)
                session['tipo_usuario'] = 'master'
                return redirect(url_for('master_bp.master'))

            # Verifica Usuario
            usuario = db.query(Usuario).filter_by(login=login_input).first()
            if usuario and check_password_hash(usuario.senha, senha_input):
                login_user(usuario)
                session['tipo_usuario'] = 'usuario'
                return redirect(url_for('usuario_bp.usuario'))

        finally:
            db.close()

        erro = "Login ou senha inválidos"
        return render_template('login.html', erro=erro)


@login_manager.user_loader
def user_loader(user_id):
    tipo = session.get('tipo_usuario')
    db = SessionLocal()
    try:
        if tipo == 'master':
            return db.get(Master, int(user_id))
        elif tipo == 'usuario':
            return db.get(Usuario, int(user_id))
        # elif tipo == 'cliente':
        #     return db.get(Cliente, int(user_id))
    finally:
        db.close()
    return None


@login_bp.route('/verificar_login', methods=['POST'])
def verificar_login():
    login = request.json.get('login')
    if not login:
        return jsonify({'disponivel': False, 'mensagem': 'Login inválido.'})

    if login_existe(login):
        return jsonify({'disponivel': False, 'mensagem': 'Login já está em uso.'})
    else:
        return jsonify({'disponivel': True, 'mensagem': 'Login disponível!'})


@login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.clear()  # Limpa tipo de usuário e demais dados da sessão
    return redirect(url_for('login_bp.login'))
