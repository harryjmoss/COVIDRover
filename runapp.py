import os
import sys
import atexit
from covidrover import app
from covidrover import update_plots
from datetime import datetime
from jinja2 import Template
from bokeh.resources import CDN
from bokeh.embed import components

from flask import Flask, request, render_template
sys.path.append(os.path.dirname(__name__))
    
def run_covidrover_plotting():
    print("Running covidrover plots setup!")
    bokeh_plots, imgfiles=update_plots.main()
    last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return bokeh_plots,imgfiles,last_update

# get initial variables from covidrover
bokeh_plots, imgfiles, last_update= run_covidrover_plotting()
last_update="Now"
app=app.create_app()
@app.route('/')
def home():
    return render_template("index.html",lastUpdate=last_update)

@app.route('/casesvsimd')
def cases_imd_2dhist():
    cmap="static/FrequencyOfCaseNumbersAsAFunctionOfImd.png"
    return render_template("plotimage.html",lastUpdate=last_update,colormap=cmap,alttext="2D Histogram of Cases vs IMD")


@app.route('/deathsvsdecile')
def deaths_vs_imd_dec():
    cmap="static/Covid-19MortalityPer100000PeopleByDeprivationDecileBetweenMarchAndMay2020.png"
    return render_template("plotimage.html",lastUpdate=last_update,colormap=cmap)

@app.route('/plotcases')
def bokeh_plot_cases():
    cmap="static/Lab-ConfirmedCovid-19CasesByAreaInEngland.html"
    return render_template("embedbokeh.html",lastUpdate=last_update,colormap=cmap)

@app.route('/plotimd')
def bokeh_plot_imd():
    cmap="static/AverageIndexOfMultipleDeprivationByLowerTierLocalAuthorityInEngland.html"
    return render_template("embedbokeh.html",lastUpdate=last_update,colormap=cmap)

@app.route('/plotimdnorm')
def bokeh_plot_imdnorm():
    cmap="static/NormalisedAverageIndexOfMultipleDeprivationByLowerTierLocalAuthorityInEngland.html"
    return render_template("embedbokeh.html",lastUpdate=last_update,colormap=cmap)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__== "__main__":
    app.run(debug=True, use_reloader=False)

