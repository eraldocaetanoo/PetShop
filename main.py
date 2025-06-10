# main.py
from flask import Flask
from controllers.utils.utils import login_manager
from controllers.usuario_controller import usuario_bp
from controllers.login_controller import login_bp
from controllers.master_controller import master_bp

app = Flask(__name__)
app.secret_key = '7b3ac914c2a7db3f836e1d5f4aa6e34e5a66f57f9e5e084f71f86ec9de0a1f94'


# Inicializa extensões

login_manager.init_app(app)
login_manager.login_view = 'login_bp.login'

# Registra Blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(login_bp)
app.register_blueprint(master_bp)

# Cria o banco se necessário e roda o servidor
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
