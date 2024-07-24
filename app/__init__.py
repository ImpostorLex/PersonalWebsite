from flask import Flask

from config import Config
from app.extensions import db, LoginManager, login_required, setup_logging
import os

from app.models.auth import Admin

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    
    setup_logging(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        
        return Admin.query.get(int(user_id))
    
   
    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Register post blueprint and add a prefix so /posts/ /posts/categories
    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')
    
    # Register auth blueprint
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
