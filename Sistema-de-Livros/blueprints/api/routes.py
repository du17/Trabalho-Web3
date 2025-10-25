from flask import jsonify, request, abort
from extensions import db
from models import Livro
from . import api_bp

# GET /api/livros - Lista todos os livros
@api_bp.route("/livros", methods=["GET"])
def api_listar_livros():
    # Suporta busca via query parameter ?q=termo
    busca = request.args.get("q", "").strip()
    
    query = Livro.query
    
    if busca:
        query = query.filter(
            (Livro.titulo.ilike(f"%{busca}%")) |
            (Livro.autor.ilike(f"%{busca}%")) |
            (Livro.isbn.ilike(f"%{busca}%"))
        )
    
    livros = query.order_by(Livro.titulo).all()
    return jsonify([livro.to_dict() for livro in livros]), 200


# GET /api/livros/<id> - Obtém um livro específico
@api_bp.route("/livros/<int:id>", methods=["GET"])
def api_obter_livro(id):
    livro = Livro.query.get_or_404(id)
    return jsonify(livro.to_dict()), 200


# POST /api/livros - Cria um novo livro
@api_bp.route("/livros", methods=["POST"])
def api_criar_livro():
    dados = request.get_json(silent=True) or {}
    
    # Valida campos obrigatórios
    if not all(k in dados for k in ("titulo", "autor")):
        abort(400, description="Campos obrigatórios: titulo, autor")
    
    # Verifica ISBN duplicado
    if dados.get("isbn") and Livro.query.filter_by(isbn=dados["isbn"]).first():
        abort(400, description="ISBN já cadastrado")
    
    livro = Livro(
        titulo=dados["titulo"],
        autor=dados["autor"],
        isbn=dados.get("isbn"),
        ano_publicacao=dados.get("ano_publicacao"),
        editora=dados.get("editora"),
        descricao=dados.get("descricao")
    )
    
    db.session.add(livro)
    db.session.commit()
    
    return jsonify(livro.to_dict()), 201


# PUT/PATCH /api/livros/<id> - Atualiza um livro
@api_bp.route("/livros/<int:id>", methods=["PUT", "PATCH"])
def api_atualizar_livro(id):
    livro = Livro.query.get_or_404(id)
    dados = request.get_json(silent=True) or {}
    
    # Verifica ISBN duplicado
    if dados.get("isbn"):
        livro_existente = Livro.query.filter_by(isbn=dados["isbn"]).first()
        if livro_existente and livro_existente.id != livro.id:
            abort(400, description="ISBN já cadastrado em outro livro")
    
    # Atualiza campos
    livro.titulo = dados.get("titulo", livro.titulo)
    livro.autor = dados.get("autor", livro.autor)
    livro.isbn = dados.get("isbn", livro.isbn)
    livro.ano_publicacao = dados.get("ano_publicacao", livro.ano_publicacao)
    livro.editora = dados.get("editora", livro.editora)
    livro.descricao = dados.get("descricao", livro.descricao)
    
    db.session.commit()
    
    return jsonify(livro.to_dict()), 200


# DELETE /api/livros/<id> - Exclui um livro
@api_bp.route("/livros/<int:id>", methods=["DELETE"])
def api_excluir_livro(id):
    livro = Livro.query.get_or_404(id)
    
    db.session.delete(livro)
    db.session.commit()
    
    return jsonify({"mensagem": "Livro excluído com sucesso"}), 200
