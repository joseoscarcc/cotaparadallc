from flask import Blueprint

bp = Blueprint('viaje', __name__)

from app.viaje import routes