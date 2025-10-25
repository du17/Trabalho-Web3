from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

# Modelo de Usuário
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    
    def set_senha(self, senha: str) -> None:
        """Define a senha do usuário com hash seguro"""
        self.senha_hash = generate_password_hash(senha)
    
    def check_senha(self, senha: str) -> bool:
        """Verifica se a senha fornecida está correta"""
        return check_password_hash(self.senha_hash, senha)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'


# Modelo de Livro
class Livro(db.Model):
    __tablename__ = 'livros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    ano_publicacao = db.Column(db.Integer)
    editora = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Livro {self.titulo}>'
    
    def to_dict(self):
        """Serializa o livro para dicionário (útil para API)"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'isbn': self.isbn,
            'ano_publicacao': self.ano_publicacao,
            'editora': self.editora,
            'descricao': self.descricao
        }
