"""Routes for flask app"""
# pylint: disable=C0301
from datetime import datetime
from flask import render_template
from flask import current_app as app


def update_timer():
    """Get the time of the latest API query"""
    last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return last_update


@app.route("/")
def home():
    """Define index route"""
    return render_template("index.html", lastUpdate=app.last_update)


@app.route("/casesvsimd")
def cases_imd_2dhist():
    """2D hist route"""
    cmap = "static/png/FrequencyOfCaseNumbersAsAFunctionOfImd.png"
    return render_template(
        "plotimage.html",
        lastUpdate=app.last_update,
        colormap=cmap,
        alttext="2D Histogram of Cases vs IMD",
    )


@app.route("/deathsvsdecile")
def deaths_vs_imd_dec():
    """Deaths vs IMD line plot route"""
    cmap = "static/png/Covid-19MortalityPer100000PeopleByDeprivationDecileBetweenMarchAndMay2020.png"
    return render_template("plotimage.html", lastUpdate=app.last_update, colormap=cmap)


@app.route("/plotcases")
def bokeh_plot_cases():
    """Cases chloropleth"""
    cmap = "static/bokeh/Lab-ConfirmedCovid-19CasesByAreaInEngland.html"
    return render_template("embedbokeh.html", lastUpdate=app.last_update, colormap=cmap)


@app.route("/plotimd")
def bokeh_plot_imd():
    """Avg IMD chloropleth"""
    cmap = "static/bokeh/AverageIndexOfMultipleDeprivationByLowerTierLocalAuthorityInEngland.html"
    return render_template("embedbokeh.html", lastUpdate=app.last_update, colormap=cmap)


@app.route("/plotimdnorm")
def bokeh_plot_imdnorm():
    """Normalised avg. IMD chloropleth"""
    cmap = "static/bokeh/NormalisedAverageIndexOfMultipleDeprivationByLowerTierLocalAuthorityInEngland.html"
    return render_template("embedbokeh.html", lastUpdate=app.last_update, colormap=cmap)


@app.errorhandler(404)
def page_not_found():
    """Handle 404 errors"""
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
