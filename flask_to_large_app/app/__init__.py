from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    from .main import main as m
    app.register_blueprint(m)
    return app
