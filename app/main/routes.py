from flask import render_template
from app.main import bp

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/privacy')
def privacy():
    return render_template('main/privacy.html')

@bp.route('/terms')
def terms():
    return render_template('main/terms.html')