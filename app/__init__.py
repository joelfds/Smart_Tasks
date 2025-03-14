# app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    from .main import bp
    app.register_blueprint(bp)

    return app
