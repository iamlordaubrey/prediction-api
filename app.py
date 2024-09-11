from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api

from api.auth_routes import auth_namespace
from config.app_config import Config
from config.db_config import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Flask-Migrate
    Migrate(app, db)

    # Initialize Flask-RESTx API
    api = Api(
        app,
        version='1.0',
        title='Prediction API',
        description='API for managing prediction models',
        doc='/api'
    )

    # Register Blueprints
    api.add_namespace(auth_namespace, path="/auth")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
