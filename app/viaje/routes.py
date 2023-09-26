from flask import render_template, jsonify,request
from app.viaje import bp
from app.extensions import db

@bp.route('/', methods=['GET', 'POST'])
def index(municipio_value=None, product_value=None):
    title="Book a trip"

   
    
    return render_template('viaje/viaje.html',title=title)


