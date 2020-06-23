from flask import Flask
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from datetime import datetime

def create_app(dev=False):
    app = Flask(__name__)
    Bootstrap(app)
    AppConfig(app)
    
    if(dev):
        app.config.from_object("config.Development")

    if app.config['TESTING']:
        print("Development server")
    else:
        print("Production server")

    testing = bool(app.testing)

    with app.app_context():
        from . import routes
        from . import update_plots
        if testing:
            app.last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            # get initial variables from covidrover
            print("Running covidrover plots setup!")
            # don't do anything with the bokeh plots or image filepaths
            # to-do
            _bokeh, _imgs = update_plots.run_covidrover()     
            app.last_update = routes.update_timer()

        return app
