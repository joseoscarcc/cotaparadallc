from flask import Blueprint

bp = Blueprint('taller', __name__)

from app.taller import routes