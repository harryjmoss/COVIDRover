import os
import sys
import atexit
from covidrover import app
from covidrover import update_plots
from datetime import datetime
from flask import Flask, request, render_template
from apscheduler.schedulers.background import BackgroundScheduler
sys.path.append(os.path.dirname(__name__))

def daily_updates():
    update_plots.main()
    last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return

# set up daily update as a background job
scheduler = BackgroundScheduler()
scheduler.add_job(func=daily_updates, trigger="interval", hours=24)
scheduler.start()


last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S')


app=app.create_app()

@app.route('/')
def home():
    return render_template("index.html",lastUpdate=last_update)

def run():
    app.run(debug=True, use_reloader=False)

run()


atexit.register(lambda: scheduler.shutdown())