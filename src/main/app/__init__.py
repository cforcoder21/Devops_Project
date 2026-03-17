from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__)
    CORS(app)

    from src.main.config.config import config
    app.config.from_object(config[config_name])

    db.init_app(app)

    from src.main.app.routes import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
