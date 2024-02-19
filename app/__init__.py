from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager  # Importando JWTManager
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key' 
    jwt = JWTManager(app)

    db.init_app(app)

    with app.app_context():
        from .routes import bp
        app.register_blueprint(bp)
        db.create_all()
        
    return app
