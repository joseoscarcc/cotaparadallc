from flask import Blueprint

bp = Blueprint('libro', __name__)

from app.libro import routes