# static/__init__.py

from flask import request, abort
from .config import Config
from static.routes import Routes


def init_app(app):
    # Initialize the Config object to load database configurations
    app.config.from_object(Config())  # This uses your custom Config class
    # app.config.from_object('api.config.Config')  # Or use your configuration class

    # Initialize routes by passing the app instance to the function
    Routes.init_routes(app)

    return app


def init_database(app):
    """Setup database initialization."""

    @app.before_request
    def initialize_database():
        config = Config()  # Optionally, pass a custom config file path
        # CREATE DATABASE
        config.check_and_create_database()
        # CREATE TABLES
        config.check_and_create_tables()
        # DROP TABLES
        # config.drop_tables()



    # @app.before_request
    # def csrf_protect():
    #     if request.method == 'POST':
    #         token = request.form.get('csrf_token')
    #         # Compare token with the session token or other method
    #         if not token or token != 'steve':
    #             abort(403)  # Forbidden if tokens don't match
