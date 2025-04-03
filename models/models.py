from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Master(db.Model):
    __tablename__ = 'master'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    login = db.Column(db.String(30), unique=True, nullable=False)
    senha = db.Column(db.String(), nullable=False)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.Integer, nullable=False)
    login = db.Column(db.String(30), unique=True, nullable=False)
    senha = db.Column(db.String(), nullable=False)
