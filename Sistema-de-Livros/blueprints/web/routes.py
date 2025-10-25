from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import web_bp
from .forms import LoginForm, RegistroForm, LivroForm
from extensions import db
from models import Usuario, Livro

# Página inicial
@web_bp.route("/")
def index():
    return render_template("index.html")


# Registro de novo usuário
@web_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("web.livros"))
    
    form = RegistroForm()
    if form.validate_on_submit():
        # Verifica se email já existe
        if Usuario.query.filter_by(email=form.email.data).first():
            flash("E-mail já cadastrado.", "warning")
            return redirect(url_for("web.registro"))
        
        # Cria novo usuário
        usuario = Usuario(nome=form.nome.data, email=form.email.data)
        usuario.set_senha(form.senha.data)
        
        db.session.add(usuario)
        db.session.commit()
        
        flash("Conta criada com sucesso! Faça login.", "success")
        return redirect(url_for("web.login"))
    
    return render_template("registro.html", form=form)


# Login de usuário
@web_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("web.livros"))
    
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        
        if usuario and usuario.check_senha(form.senha.data):
            login_user(usuario)
            flash(f"Bem-vindo, {usuario.nome}!", "success")
            
            # Redireciona para página solicitada ou para livros
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("web.livros"))
        
        flash("Credenciais inválidas.", "danger")
    
    return render_template("login.html", form=form)


# Logout
@web_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("web.login"))


# Lista de livros com busca
@web_bp.route("/livros")
@login_required
def livros():
    # Captura parâmetro de busca
    busca = request.args.get("q", "").strip()
    
    query = Livro.query
    
    if busca:
        # Busca por título, autor ou ISBN
        query = query.filter(
            (Livro.titulo.ilike(f"%{busca}%")) |
            (Livro.autor.ilike(f"%{busca}%")) |
            (Livro.isbn.ilike(f"%{busca}%"))
        )
    
    livros = query.order_by(Livro.titulo).all()
    
    return render_template("livros.html", livros=livros, busca=busca)


# Criar novo livro
@web_bp.route("/livros/novo", methods=["GET", "POST"])
@login_required
def novo_livro():
    form = LivroForm()
    
    if form.validate_on_submit():
        # Verifica se ISBN já existe
        if form.isbn.data and Livro.query.filter_by(isbn=form.isbn.data).first():
            flash("ISBN já cadastrado.", "warning")
            return redirect(url_for("web.novo_livro"))
        
        livro = Livro(
            titulo=form.titulo.data,
            autor=form.autor.data,
            isbn=form.isbn.data,
            ano_publicacao=form.ano_publicacao.data,
            editora=form.editora.data,
            descricao=form.descricao.data
        )
        
        db.session.add(livro)
        db.session.commit()
        
        flash(f"Livro '{livro.titulo}' cadastrado com sucesso!", "success")
        return redirect(url_for("web.livros"))
    
    return render_template("livro_form.html", form=form, titulo="Novo Livro")


# Editar livro
@web_bp.route("/livros/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_livro(id):
    livro = Livro.query.get_or_404(id)
    form = LivroForm(obj=livro)
    
    if form.validate_on_submit():
        # Verifica se ISBN já existe em outro livro
        if form.isbn.data:
            livro_existente = Livro.query.filter_by(isbn=form.isbn.data).first()
            if livro_existente and livro_existente.id != livro.id:
                flash("ISBN já cadastrado em outro livro.", "warning")
                return redirect(url_for("web.editar_livro", id=id))
        
        livro.titulo = form.titulo.data
        livro.autor = form.autor.data
        livro.isbn = form.isbn.data
        livro.ano_publicacao = form.ano_publicacao.data
        livro.editora = form.editora.data
        livro.descricao = form.descricao.data
        
        db.session.commit()
        
        flash(f"Livro '{livro.titulo}' atualizado com sucesso!", "success")
        return redirect(url_for("web.livros"))
    
    return render_template("livro_form.html", form=form, titulo="Editar Livro", livro=livro)


# Excluir livro
@web_bp.route("/livros/<int:id>/excluir", methods=["POST"])
@login_required
def excluir_livro(id):
    livro = Livro.query.get_or_404(id)
    titulo = livro.titulo
    
    db.session.delete(livro)
    db.session.commit()
    
    flash(f"Livro '{titulo}' excluído com sucesso!", "info")
    return redirect(url_for("web.livros"))


# Visualizar detalhes do livro
@web_bp.route("/livros/<int:id>")
@login_required
def ver_livro(id):
    livro = Livro.query.get_or_404(id)
    return render_template("livro_detalhes.html", livro=livro)
