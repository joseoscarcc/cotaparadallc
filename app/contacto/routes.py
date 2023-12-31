from flask import render_template,request, flash
from app.contacto import bp
from app.extensions import db
from app.models.cpschema import Contacto
from datetime import datetime

@bp.route('/')
def index():
    title="Contacto"
    
    
    return render_template('contacto/contacto.html',title=title)

@bp.route('/submit', methods=['POST'])
def submit():
    name = request.form['nombre']
    email = request.form['correo']
    phone = request.form['telefono']
    message = request.form['message']

    # Create an Contacto instance
    order = Contacto(
        name=name,
        timestamp=datetime.utcnow(),  # You may need to import datetime
        email=email,
        phone=phone,  # Status set to 1 as you mentioned
        message=message
    )

    # # Add these instances to the session and commit the changes
    db.session.add(order)
    db.session.commit()

    flash('Forma enviada correctamente')
    return render_template('contacto/contacto.html')
