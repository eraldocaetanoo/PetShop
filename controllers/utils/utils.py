from flask import render_template, request, redirect, url_for, session, abort, flash, send_file
from werkzeug.security import generate_password_hash
from flask_login import LoginManager
from functools import wraps
from models.models import *
from sqlalchemy.orm import sessionmaker
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime


# Configura a sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Inicialização do LoginManager
login_manager = LoginManager()

# Decorator para tipo de usuário
def tipo_usuario_requerido(tipo):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if session.get('tipo_usuario') != tipo:
                abort(403)  # Proibido
            return func(*args, **kwargs)
        return decorated_view
    return wrapper

# Verifica se login já existe
def login_existe(login):
    with SessionLocal() as db:
        if db.query(Master).filter_by(login=login).first():
            return True
        if db.query(Usuario).filter_by(login=login).first():
            return True
    return False

# Cadastro de usuário
def cadastrar_usuario(logado_tipo):
    if request.method == 'GET':
        return render_template('usuario/cadastroUsuario.html')

    elif request.method == 'POST':
        nome = request.form['usuarioNome']
        login = request.form['usuarioLogin']
        senha = request.form['usuarioSenha']
        email = request.form['usuarioEmail']
        telefone = request.form['usuarioTelefone']
        senha_hash = generate_password_hash(senha)

        if login_existe(login):
            return render_template('usuario/cadastroUsuario.html', erro="Login já em uso.")

        usuario = Usuario(nome=nome, login=login, senha=senha_hash, email=email, telefone=telefone)
        with SessionLocal() as db:
            db.add(usuario)
            db.commit()

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for(f'{logado_tipo}_bp.cadastro_usuario'))

# Cadastro de cliente
def cadastrar_cliente(logado_tipo):
    if request.method == 'GET':
        return render_template('cliente/cadastroCliente.html')

    elif request.method == 'POST':
        cliente = Cliente(
            nome=request.form['clienteNome'],
            genero=request.form['clienteGenero'],
            email=request.form['clienteEmail'],
            telefone=request.form['clienteTelefone'],
            rua=request.form['clienteLogradouro'],
            numero=request.form['clienteNumero'],
            bairro=request.form['clienteBairro'],
            cidade=request.form['clienteCidade'],
            estado=request.form['clienteEstado'],
            cep=request.form['clienteCep']
        )
        with SessionLocal() as db:
            db.add(cliente)
            db.commit()

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for(f'{logado_tipo}_bp.cadastro_cliente'))

# Cadastro de animal
def cadastrar_animal(logado_tipo):
    if request.method == 'GET':
        with SessionLocal() as db:
            clientes = db.query(Cliente).all()
            return render_template('animal/cadastroAnimal.html', clientes=clientes)

    elif request.method == 'POST':
        anos = int(request.form['animalIdadeAnos'] or 0)
        meses = int(request.form['animalIdadeMeses'] or 0)
        idade = anos * 12 + meses

        animal = Animais(
            nome=request.form['animalNome'],
            especie=request.form['animalEspecie'],
            raca=request.form['animalRaca'],
            idade=idade,
            sexo=request.form['animalSexo'],
            cor=request.form['animalCor'],
            peso=float(request.form['animalPeso'] or 0.0),
            responsavel_id=request.form['animalResponsavel'],
            observacoes=request.form['animalObservacoes']
        )

        with SessionLocal() as db:
            db.add(animal)
            db.commit()

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for(f'{logado_tipo}_bp.cadastro_animal'))

# Cadastro de tipo de serviço
def cadastrar_tipo_servico(logado_tipo):
    if request.method == 'GET':
        return render_template('servicos/cadastroTipoServico.html')

    elif request.method == 'POST':
        preco_str = request.form['servicoPreco']
        preco_limpo = preco_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
        preco = float(preco_limpo)

        tipo_servico = TipoServico(
            nome_servico=request.form['servicoNome'],
            descricao=request.form['servicoDescricao'],
            duracao=request.form['servicoDuracao'],
            preco=preco,
            observacoes=request.form['servicoObservacoes']
        )

        with SessionLocal() as db:
            db.add(tipo_servico)
            db.commit()

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for(f'{logado_tipo}_bp.cadastro_tipo_servico'))

# Retorna lista de usuários
def obter_cadastros(tipo):
    with SessionLocal() as db:
        return db.query(tipo).all()

# Mantém a função de renderizar HTML normalmente
def renderizar_lista_usuarios():
    usuarios = obter_cadastros(Usuario)
    return render_template('master/listar_usuarios.html', usuarios=usuarios)

def renderizar_lista_clientes():
    clientes = obter_cadastros(Cliente)
    return render_template('cliente/listar_clientes.html', clientes=clientes)


def gerar_pdf_html(template_path, context):
    html = render_template(template_path, **context)
    resultado = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), resultado)

    if not pdf.err:
        resultado.seek(0)
        return resultado
    return None

    

def gerar_relatorio(tipo):
    with SessionLocal() as db:
        context = {
            "current_date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        if tipo == "usuario":
            context["usuario"] = obter_cadastros(Usuario)
            template = "master/relatorio_usuarios.html"
            nome_arquivo = "relatorio_usuarios.pdf"
        elif tipo == "cliente":
            context["cliente"] = obter_cadastros(Cliente)
            template = "cliente/relatorio_clientes.html"  #Tem que alterar
            nome_arquivo = "relatorio_clientes.pdf"
        else:
            return None, "Tipo de relatório inválido"

        pdf_file = gerar_pdf_html(template, context)
        return pdf_file, nome_arquivo