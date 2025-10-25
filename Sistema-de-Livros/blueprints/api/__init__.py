from flask import Blueprint

# Blueprint para API RESTful (JSON)
api_bp = Blueprint("api", __name__)

from . import routes
