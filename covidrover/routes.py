from datetime import datetime
from jinja2 import Template
from flask import render_template
from flask import current_app as app

def update_timer():
    last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return last_update

@app.route('/')
def home():
    return render_template("index.html",lastUpdate=app.last_update)

@app.route('/casesvsimd')
def cases_imd_2dhist():
    cmap="static/png/FrequencyOfCaseNumbersAsAFunctionOfImd.png"
    return render_template("plotimage.html",lastUpdate=app.last_update,colormap=cmap,alttext="2D Histogram of Cases vs IMD")


@app.route('/deathsvsdecile')
def deaths_vs_imd_dec():
    cmap="static/png/Covid-19MortalityPer100000PeopleByDeprivationDecileBetweenMarchAndMay2020.png"
    return render_template("plotimage.html",lastUpdate=app.last_update,colormap=cmap)

@app.route('/plotcases')
def bokeh_plot_cases():
    cmap="static/bokeh/Lab-ConfirmedCovid-19CasesByAreaInEngland.html"
    return render_template("embedbokeh.html",lastUpdate=app.last_update,colormap=cmap)

@app.route('/plotimd')
def bokeh_plot_imd():
    cmap="static/bokeh/AverageIndexOfMultipleDeprivationByLowerTierLocalAuthorityInEngland.html"
    return render_template("embedbokeh.html",lastUpdate=app.last_update,colormap=cmap)

@app.route('/plotimdnorm')
def bokeh_plot_imdnorm():
    cmap="static/bokeh/NormalisedAverageIndexOfMultipleDeprivationByLowerTierLocalAuthorityInEngland.html"
    return render_template("embedbokeh.html",lastUpdate=app.last_update,colormap=cmap)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


