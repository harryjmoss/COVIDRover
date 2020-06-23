from flask import Flask
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    AppConfig(app)
    return app

