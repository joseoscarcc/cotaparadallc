from flask import render_template, jsonify,request
from app.libro import bp
from app.extensions import db



@bp.route('/')
def index():
    title="Libro - Book"

    
    return render_template('libro/libro.html',title=title)

@bp.route('/book')
def book_usa():
    title="USA - Book"

    
    return render_template('libro/book_usa.html',title=title)

@bp.route('/libro')
def libro_mex():
    title="Libro - MEX"

    
    return render_template('libro/libro_mex.html',title=title)

@bp.route('/meetus')
def libro_mex():
    title="Meet Us"

    
    return render_template('libro/meetus.html',title=title)