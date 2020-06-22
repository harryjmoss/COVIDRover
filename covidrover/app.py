from flask import Flask
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask import Flask, request, render_template

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    AppConfig(app)
    return app

