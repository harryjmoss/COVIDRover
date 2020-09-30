# pylint: disable=C0415
"""Defines flask app"""
from datetime import datetime
from flask import Flask
from flask_bootstrap import Bootstrap


def create_app(dev=False):
    """Create app and return app object"""
    app = Flask(__name__)
    Bootstrap(app)

    if dev:
        app.config.from_object("config.Development")

    if app.config["TESTING"]:
        print("Development server")
    else:
        print("Production server")

    testing = bool(app.testing)

    with app.app_context():
        from . import routes
        from . import update_plots

        if testing:
            app.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            # get initial variables from covidrover
            print("Running covidrover plots setup!")
            # don't do anything with the bokeh plots or image filepaths
            # to-do
            _out_plots = update_plots.run_covidrover()
            app.last_update = routes.update_timer()

        return app
