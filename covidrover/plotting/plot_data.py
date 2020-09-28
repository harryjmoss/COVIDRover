# pylint: disable=E1121,R0913,R0914
"""Plotting functions to handle 2D histograms, line plots with
error bands and chloropleth plots.
"""
import numpy as np
import matplotlib.pyplot as plt

# bokeh imports...
from bokeh.io import output_file, save
from bokeh.plotting import figure
import bokeh.palettes
from bokeh.models import (
    GeoJSONDataSource,
    LinearColorMapper,
    LogColorMapper,
    ColorBar,
    HoverTool,
)
from bokeh.models.tickers import FixedTicker, BasicTicker


def plot_2d_hist(
    geodataframe, hist_title, xvar, yvar, xbins, ybins, mincases=1, write_file=True
):
    """Plot 2D hist of cases vs IMD"""
    # set up figure and axis objects
    plt.ioff()  # turn off interactive mode
    plt.figure()
    axis = plt.gca()
    # Creates a right-hand axis with fractional size of ax and with fixed padding
    plt.figure(1)
    axis = plt.gca()
    # get numpy arrays out of dataframe
    xdata = geodataframe[xvar].to_numpy()
    ydata = geodataframe[yvar].to_numpy()
    nbins = [xbins, ybins]
    axis.set_yticks(ybins)
    axis.set_xticks(xbins)
    # plot the 2d hist with the variables specified
    two_dim_hist = axis.hist2d(xdata, ydata, bins=nbins, cmin=mincases, cmap="viridis")
    # label the axes
    plt.xlabel(xvar, fontsize=12)
    plt.ylabel(yvar, fontsize=12)
    plt.title(hist_title, fontsize=14)
    # add a nice colour bar
    cbar = plt.colorbar(two_dim_hist[3], ax=axis)
    # set a label for the colour bar
    cbar.axis.set_ylabel("Number of events", labelpad=15, rotation=270)
    # sorts out padding, just aesthetic
    plt.tight_layout()
    output_file_name = "output/png/" + hist_title.title().replace(" ", "") + ".png"
    web_file_name = (
        "covidrover/static/png/" + hist_title.title().replace(" ", "") + ".png"
    )

    if write_file:
        plt.savefig(output_file_name, dpi=300)
        plt.savefig(web_file_name, dpi=300)

    return web_file_name


def plot_deaths_imd_decile(
    deaths_imd, hist_title, xaxis_label, yaxis_label, write_file=True
):
    """Plot deaths by IMD decile"""
    # Sort the dataframe into All, Women, Men
    deaths_imd_all = deaths_imd[deaths_imd["Sex"].str.match("Persons")].drop(
        columns="Sex"
    )
    deaths_imd_men = deaths_imd[deaths_imd["Sex"].str.match("Males")].drop(
        columns="Sex"
    )
    deaths_imd_women = deaths_imd[deaths_imd["Sex"].str.match("Females")].drop(
        columns="Sex"
    )

    # set up figure and axis
    plt.figure(None, [10, 8])  # figure number, [width,height (inches)]
    plt.ioff()  # turn off interactive mode and stop matplotlib trying to display plots
    axis = plt.gca()

    # Plot the lines of the mean fatality rate for All people, women and men
    # Also plot the 95% CI error band around the mean
    # Blank/filled labels for the bands is just stylistic
    plt.plot(
        deaths_imd_all["Decile"].tolist(),
        deaths_imd_all["Rate"].tolist(),
        "Green",
        label="All",
    )
    plt.fill_between(
        deaths_imd_all["Decile"].tolist(),
        deaths_imd_all["LowerCI"],
        deaths_imd_all["UpperCI"],
        color="Green",
        alpha=0.5,
        label=" ",
    )
    plt.plot(
        deaths_imd_women["Decile"].tolist(),
        deaths_imd_women["Rate"].tolist(),
        "Orange",
        label="Women",
    )
    plt.fill_between(
        deaths_imd_women["Decile"].tolist(),
        deaths_imd_women["LowerCI"],
        deaths_imd_women["UpperCI"],
        color="Orange",
        alpha=0.5,
        label="95% CI",
    )
    plt.plot(
        deaths_imd_men["Decile"].tolist(),
        deaths_imd_men["Rate"].tolist(),
        "Red",
        label="Men",
    )
    plt.fill_between(
        deaths_imd_men["Decile"].tolist(),
        deaths_imd_men["LowerCI"],
        deaths_imd_men["UpperCI"],
        color="Red",
        alpha=0.5,
        label=" ",
    )

    # set title, ticks, labels
    plt.title(hist_title)
    axis.set_ylabel(xaxis_label)
    axis.set_xlabel(yaxis_label)
    axis.set_xticks(np.arange(0, 11))
    plt.legend(loc="upper right")

    output_file_name = "output/png/" + hist_title.title().replace(" ", "") + ".png"
    web_file_name = (
        "covidrover/static/png/" + hist_title.title().replace(" ", "") + ".png"
    )
    # write file
    if write_file:
        plt.savefig(output_file_name, dpi=300)
        plt.savefig(web_file_name, dpi=300)

    return web_file_name


def plot_chloropleth(
    json_map_df,
    plotfield,
    plot_title,
    hover_fields,
    cbar_low_y,
    cbar_high_y,
    save_output=True,
    custom_ticks=None,
    log_color=False,
):
    """Plot chloropleth plots"""
    geosource = GeoJSONDataSource(geojson=json_map_df)
    if custom_ticks is not None:
        # create colour bar with custom tick labels if provided
        cbar_ticker = FixedTicker(ticks=custom_ticks)
        palette = bokeh.palettes.viridis(len(custom_ticks))
    else:
        cbar_ticker = BasicTicker()
        palette = bokeh.palettes.viridis(10)
    palette = palette[::-1]
    if log_color:
        color_mapper = LogColorMapper(palette=palette, low=cbar_low_y, high=cbar_high_y)

    else:
        # Map range of numbers to a colour palette
        color_mapper = LinearColorMapper(
            palette=palette, low=cbar_low_y, high=cbar_high_y
        )

    # Add a hover tooltip on final plot
    # expects a dictionary of hover fields items
    fields_tuple = list(hover_fields.items())
    hover = HoverTool(tooltips=fields_tuple)

    # Create a colour bar with default tick labels
    color_bar = ColorBar(
        color_mapper=color_mapper,
        ticker=cbar_ticker,
        label_standoff=8,
        width=500,
        height=20,
        border_line_color=None,
        location=(0, 0),
        orientation="horizontal",
    )
    # Start plotting!
    map_plot = figure(
        title=plot_title,
        plot_height=700,
        plot_width=500,
        toolbar_location=None,
        tools=[hover],
    )
    # p.add_tile(tile_provider)
    map_plot.xgrid.grid_line_color = None
    map_plot.ygrid.grid_line_color = None
    # Add patch renderer to figure.
    map_plot.patches(
        "xs",
        "ys",
        source=geosource,
        fill_color={"field": plotfield, "transform": color_mapper},
        line_color="black",
        line_width=0.1,
        fill_alpha=0.8,
    )
    # Specify figure layout.
    map_plot.add_layout(color_bar, "below")
    map_plot.xaxis.visible = False
    map_plot.yaxis.visible = False
    # Save the figure
    outfile_name = (
        "covidrover/static/bokeh/" + plot_title.title().replace(" ", "") + ".html"
    )
    if save_output:
        output_file(outfile_name)
        save(map_plot)
    return outfile_name


def setup_plots():
    """Set up variables to include in chloropleth plots"""
    print("Generating plots...")
    hover_fields_standard = {
        "Date": "@Date",
        "Area": "@Area",
        "Average IMD": "@IMD",
        "New cases": "@NewCases",
        "Total cases": "@TotalCases",
        "Cases per 100k": "@CasesPer100k",
        "New deaths": "@NewDeaths",
        "Total deaths": "@TotalDeaths",
        "Deaths per 100k": "@DeathsPer100k",
    }
    hover_fields_imd_norm = {
        "Date": "@Date",
        "Area": "@Area",
        "Normalised Average IMD": "@IMDNorm",
        "New cases": "@NewCases",
        "Total cases": "@TotalCases",
        "Cases per 100k": "@CasesPer100k",
        "New deaths": "@NewDeaths",
        "Total deaths": "@TotalDeaths",
        "Deaths per 100k": "@DeathsPer100k",
    }

    return hover_fields_standard, hover_fields_imd_norm
