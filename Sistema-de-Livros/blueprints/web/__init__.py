from flask import Blueprint

# Blueprint para rotas web (interface HTML)
web_bp = Blueprint("web", __name__, template_folder="../../templates")

from . import routes
