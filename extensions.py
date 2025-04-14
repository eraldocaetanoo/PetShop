# extensions.py
from flask_login import LoginManager
from models.models import Master, Usuario

from flask import session, abort


from functools import wraps


login_manager = LoginManager()

def tipo_usuario_requerido(tipo):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if session.get('tipo_usuario') != tipo:
                abort(403)  # Proibido
            return func(*args, **kwargs)
        return decorated_view
    return wrapper




def login_existe(login):
    if Master.query.filter_by(login=login).first():
        return True
    if Usuario.query.filter_by(login=login).first():
        return True
    
    return False
