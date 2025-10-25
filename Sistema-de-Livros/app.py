from flask import Flask
from config import Config
from extensions import db, login_manager
from models import Usuario
from blueprints.web import web_bp
from blueprints.api import api_bp

def create_app():
    """Fábrica da aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    
    # Callback para carregar usuário
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Registra blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    
    # Cria tabelas no banco (apenas para desenvolvimento)
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
