from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Master(UserMixin, db.Model):
    __tablename__ = 'master'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    login = db.Column(db.String(30), unique=True, nullable=False)
    senha = db.Column(db.String(), nullable=False)

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    login = db.Column(db.String(30), unique=True, nullable=False)
    senha = db.Column(db.String(), nullable=False)

class Cliente(UserMixin, db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    # Endereço separado
    rua = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    cep = db.Column(db.String(20), nullable=False)

class Animais(UserMixin, db.Model):
    __tablename__ = 'animais'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(100), nullable=False)
    raca = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=True) 
    sexo = db.Column(db.String(100), nullable=False)
    cor = db.Column(db.String(100), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    responsavel_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    responsavel = db.relationship('Cliente', backref='animais')
    observacoes = db.Column(db.String(100), nullable=False)

class Veterinarios(UserMixin, db.Model):
    __tablename__ = 'veterinarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=True)
    genero = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    formacao = db.Column(db.String(100), nullable=False)
    especializacao = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(30), unique=True, nullable=False)
    senha = db.Column(db.String(), nullable=False)

class Prontuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    responsavel = db.Column(db.String(100), nullable=False)
    servicos_realizados = db.Column(db.String(100), nullable=False)

class ServicosRealizados(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servicos_realizados = db.Column(db.String(100), nullable=False)
    nome_animal = db.Column(db.String(100), nullable=False)
    veterinario = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=True)
    valor = db.Column(db.Float, nullable=False)
    tipo_servico = db.Column(db.String(100), nullable=False)

class TipoServico(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_servico = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    duracao = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    observacoes = db.Column(db.String(100), nullable=False)
