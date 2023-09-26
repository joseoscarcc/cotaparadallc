from flask import Blueprint

bp = Blueprint('checkoutmp', __name__)

from app.checkoutmp import routes