# main.py
from flask import Flask
from extensions import login_manager
import os
from models.models import db
from controllers.usuario_controller import usuario_bp
from controllers.login_controller import login_bp
from controllers.master_controller import master_bp

app = Flask(__name__)
app.secret_key = '7b3ac914c2a7db3f836e1d5f4aa6e34e5a66f57f9e5e084f71f86ec9de0a1f94'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensões
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login_bp.login'

# Registra Blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(login_bp)
app.register_blueprint(master_bp)

# Cria o banco se necessário e roda o servidor
if __name__ == '__main__':
    if not os.path.exists('database.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True, host='0.0.0.0')
