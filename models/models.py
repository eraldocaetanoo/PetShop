from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

from models.conexao import *



class Master(UserMixin, Base):
    __tablename__ = 'master'
    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    nome = Column("nome", String(100), unique=True, nullable=False)
    login = Column("login", String(30), unique=True, nullable=False)
    senha = Column("senha", String(255), nullable=False)

class Usuario(UserMixin, Base):
    __tablename__ = 'usuario'
    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    email = Column("email", String(100), nullable=False)
    telefone = Column("telefone", String(20), nullable=False)
    login = Column("login", String(30), unique=True, nullable=False)
    senha = Column("senha", String(255), nullable=False)

class Cliente(UserMixin, Base):
    __tablename__ = 'cliente'
    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    genero = Column("genero", String(100), nullable=False)
    email = Column("email", String(100), nullable=False)
    telefone = Column("telefone", String(20), nullable=False)

    # Endereço separado
    rua = Column("rua", String(100), nullable=False)
    numero = Column("numero", String(20), nullable=False)
    bairro = Column("bairro", String(100), nullable=False)
    cidade = Column("cidade", String(100), nullable=False)
    estado = Column("estado", String(100), nullable=False)
    cep = Column("cep", String(20), nullable=False)

class Animais(UserMixin, Base):
    __tablename__ = 'animais'
    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    especie = Column("especie", String(100), nullable=False)
    raca = Column("raca", String(100), nullable=False)
    idade = Column("idade", Integer, nullable=True) 
    sexo = Column("sexo", String(100), nullable=False)
    cor = Column("cor", String(100), nullable=False)
    peso = Column("peso", Float, nullable=False)
    responsavel_id = Column("responsavel_id", Integer, ForeignKey('cliente.id'), nullable=False)
    responsavel = relationship('Cliente', backref='animais')
    observacoes = Column("observacoes", String(100), nullable=False)

class Veterinarios(UserMixin, Base):
    __tablename__ = 'veterinarios'
    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    data_nascimento = Column("data_nascimento", Date, nullable=True)
    genero = Column("genero", String(100), nullable=False)
    email = Column("email", String(100), nullable=False)
    telefone = Column("telefone", String(20), nullable=False)
    formacao = Column("formacao", String(100), nullable=False)
    especializacao = Column("especializacao", String(100), nullable=False)
    observacoes = Column("observacoes", String(100), nullable=False)
    login = Column("login", String(30), unique=True, nullable=False)
    senha = Column("senha", String(255), nullable=False)

class Prontuario(UserMixin, Base):
    __tablename__ = 'prontuario'
    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    responsavel = Column("responsavel", String(100), nullable=False)
    servicos_realizados = Column("servicos_realizados", String(100), nullable=False)

class ServicosRealizados(UserMixin, Base):
    __tablename__ = 'servicos_realizados'
    id = Column("id", Integer, primary_key=True)
    servicos_realizados = Column("servicos_realizados", String(100), nullable=False)
    nome_animal = Column("nome_animal", String(100), nullable=False)
    veterinario = Column("veterinario", String(100), nullable=False)
    data = Column("data", Date, nullable=True)
    valor = Column("valor", Float, nullable=False)
    tipo_servico = Column("tipo_servico", String(100), nullable=False)

class TipoServico(UserMixin, Base):
    __tablename__ = 'tipo_servico'
    id = Column("id", Integer, primary_key=True)
    nome_servico = Column("nome_servico", String(100), nullable=False)
    descricao = Column("descricao", String(100), nullable=False)
    duracao = Column("duracao", String(100), nullable=False)
    preco = Column("preco", Float, nullable=False)
    observacoes = Column("observacoes", String(100), nullable=False)

class Veterinario(UserMixin, Base):
    __tablename__ = 'veterinario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Informações Pessoais
    nome = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    sexo = Column(String(20), nullable=False)
    estado_civil = Column(String(20), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    rg = Column(String(20), unique=True, nullable=False)

    # Endereço
    endereco = Column(String(200), nullable=False)
    estado = Column(String(100), nullable=False)  # ou String(2) se usar sigla do estado

    # Contato
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Formação e Experiência
    instituicao = Column(String(100), nullable=False)
    ano_conclusao = Column(String(4), nullable=False)
    crmv = Column(String(50), unique=True, nullable=False)
    especializacao = Column(String(100), nullable=True)
    experiencia = Column(String(500), nullable=True)

    # Documentação enviada
    comprovante_endereco = Column(String(255), nullable=True)
    foto = Column(String(255), nullable=True)

    # Dados de Acesso
    usuario = Column(String(30), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)



# Criando as tabelas no banco de dados (caso não existam)
Base.metadata.create_all(bind=engine)