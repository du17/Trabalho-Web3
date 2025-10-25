import os

# Classe de configuração centralizada para a aplicação Flask
class Config:
    # Chave secreta para sessões e CSRF
    SECRET_KEY = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
    
    # URL de conexão com o banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        # Padrão para SQLite (mais simples para começar)
        "sqlite:///livros.db"
        # Para MySQL: "mysql+pymysql://usuario:senha@localhost/livros"
        # Para PostgreSQL: "postgresql+psycopg2://usuario:senha@localhost/livros"
    )
    
    # Desativa monitoramento de modificações (reduz overhead)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de upload (caso necessário no futuro)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
