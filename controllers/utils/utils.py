from flask import render_template, request, redirect, url_for, session, abort, flash
from models.models import db, Master, Usuario, Cliente, Animais, TipoServico
from werkzeug.security import generate_password_hash
from flask_login import LoginManager
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
        db.session.add(usuario)
        db.session.commit()
        flash("Cadastro realizado com sucesso!", "success")
        # Redireciona de volta para a página certa dependendo do tipo de usuário logado
        if logado_tipo == 'master':
            return redirect(url_for('master_bp.cadastro_usuario'))
        if logado_tipo == 'usuario':
            return redirect(url_for('usuario_bp.cadastro_usuario'))




def cadastrar_cliente(logado_tipo):
    if request.method == 'GET':
        return render_template('cliente/cadastroCliente.html')
    elif request.method == 'POST':
        nome = request.form['clienteNome']
        genero = request.form['clienteGenero']
        email = request.form['clienteEmail']
        telefone = request.form['clienteTelefone']
        rua = request.form['clienteLogradouro']
        numero = request.form['clienteNumero']
        bairro = request.form['clienteBairro']
        cidade = request.form['clienteCidade']
        estado = request.form['clienteEstado']
        cep = request.form['clienteCep']
        

        cliente = Cliente(nome=nome, genero=genero, email=email, telefone=telefone, rua=rua, numero=numero, bairro=bairro, cidade=cidade, estado=estado, cep=cep)
        db.session.add(cliente)
        db.session.commit()


        flash("Cadastro realizado com sucesso!", "success")
        # Redireciona de volta para a página certa dependendo do tipo de usuário logado
        if logado_tipo == 'master':
            return redirect(url_for('master_bp.cadastro_cliente'))
        if logado_tipo == 'usuario':
            return redirect(url_for('usuario_bp.cadastro_cliente'))



def cadastrar_animal(logado_tipo):
    if request.method == 'GET':
        clientes = Cliente.query.all()
        return render_template('animal/cadastroAnimal.html', clientes=clientes)
    elif request.method == 'POST':
        nome = request.form['animalNome']
        especie = request.form['animalEspecie']
        raca = request.form['animalRaca']
        idade = request.form['animalIdade']
        sexo = request.form['animalSexo']
        cor = request.form['animalCor']
        peso = request.form['animalPeso']
        responsavel_id = request.form['animalResponsavel']
        observacoes = request.form['animalObservacoes']
        

        animal = Animais(nome=nome, especie=especie, raca=raca, idade=idade, sexo=sexo,cor=cor, peso=peso, responsavel_id=responsavel_id, observacoes=observacoes)
        db.session.add(animal)
        db.session.commit()

        
        flash("Cadastro realizado com sucesso!", "success")
        # Redireciona de volta para a página certa dependendo do tipo de usuário logado
        if logado_tipo == 'master':
            return redirect(url_for('master_bp.cadastro_animal'))
        if logado_tipo == 'usuario':
            return redirect(url_for('usuario_bp.cadastro_animal'))


def cadastrar_tipo_servico(logado_tipo):
    if request.method == 'GET':
        return render_template('servicos/cadastroTipoServico.html')
    elif request.method == 'POST':
        nome_servico = request.form['servicoNome']
        descricao = request.form['servicoDescricao']
        duracao = request.form['servicoDuracao']
        # Exemplo: 'R$ 1.234,56' → 1234.56
        preco_str = request.form['servicoPreco']
        preco_limpo = preco_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
        preco = float(preco_limpo)
        observacoes = request.form['servicoObservacoes']
        

        tipo_servico = TipoServico(nome_servico=nome_servico, descricao=descricao, duracao=duracao, preco=preco, observacoes=observacoes)
        db.session.add(tipo_servico)
        db.session.commit()


        flash("Cadastro realizado com sucesso!", "success")
        # Redireciona de volta para a página certa dependendo do tipo de usuário logado
        if logado_tipo == 'master':
            return redirect(url_for('master_bp.cadastro_tipo_servico'))
        if logado_tipo == 'usuario':
            return redirect(url_for('usuario_bp.cadastro_tipo_servico'))

