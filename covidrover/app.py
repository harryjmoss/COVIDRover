from flask import Flask
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask import Flask, request, render_template

def main(output_files):

    def create_app():
        app = Flask(__name__)
        Bootstrap(app)
        AppConfig(app)
        return app

    app =create_app()

    @app.route('/')
    def index():
        return render_template("index.html")

    def run():
        app.run(debug=True, use_reloader=True)

    run()
