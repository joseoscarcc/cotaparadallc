from flask import render_template, jsonify,request
from app.contacto import bp
from app.extensions import db



@bp.route('/')
def index():
    title="Contacto"
    
    
    return render_template('contacto/contacto.html',title=title)


