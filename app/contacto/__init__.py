from flask import Blueprint

bp = Blueprint('contacto', __name__)

from app.contacto import routes