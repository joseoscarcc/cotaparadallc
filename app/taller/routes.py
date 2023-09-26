from flask import render_template, jsonify,request
from app.taller import bp
from app.extensions import db



@bp.route('/', methods=['GET', 'POST'])
def index():
    title="TALLERES"
    
    return render_template('taller/taller.html',title=title)


