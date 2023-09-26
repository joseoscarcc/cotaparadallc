from flask import Flask

from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Flask extensions here
    db.init_app(app)
    
    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.contacto import bp as contacto_bp
    app.register_blueprint(contacto_bp, url_prefix='/contacto')

    from app.checkoutmp import bp as checkoutmp_bp
    app.register_blueprint(checkoutmp_bp, url_prefix='/checkoutmp')

    from app.checkoutstripe import bp as checkoutstripe_bp
    app.register_blueprint(checkoutstripe_bp, url_prefix='/checkoutstripe')

    from app.libro import bp as libro_bp
    app.register_blueprint(libro_bp, url_prefix='/libro')

    return app