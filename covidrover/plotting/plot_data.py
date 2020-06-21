import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# bokeh imports...
from bokeh.io import show, output_file, save
from bokeh.plotting import figure
import bokeh.palettes
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, HoverTool
from bokeh.models.tickers import FixedTicker, BasicTicker



def plot_2d_hist(geodataframe,hist_title,xvar,yvar,xbins,ybins,mincases=1,write_file=True):
    # set up figure and axis objects    
    plt.figure()
    ax=plt.gca()
    # Creates a right-hand axis with fractional size of ax and with fixed padding
    plt.figure(1)
    ax=plt.gca()
    # get numpy arrays out of dataframe
    xdata = geodataframe[xvar].to_numpy()
    ydata = geodataframe[yvar].to_numpy()
    nbins=[xbins,ybins]
    ax.set_yticks(ybins)
    ax.set_xticks(xbins)
    # plot the 2d hist with the variables specified
    two_dim_hist=ax.hist2d(xdata,ydata,bins=nbins,cmin=mincases,cmap='viridis')
    # label the axes
    plt.xlabel(xvar, fontsize=12)
    plt.ylabel(yvar, fontsize=12)
    plt.title(hist_title, fontsize=14)
    # add a nice colour bar
    cbar=plt.colorbar(two_dim_hist[3],ax=ax)
    # set a label for the colour bar
    cbar.ax.set_ylabel('Number of events',labelpad=15,rotation=270)
    plt.tight_layout()

    if(write_file):
        output_file_name = "output/png/"+hist_title.title().replace(' ','')+".png"
        plt.savefig(output_file_name,dpi=300)
    return two_dim_hist


def plot_chloropleth(json_map_df,plotfield,plot_title,hover_fields,cbar_low_y,cbar_high_y,save_output=True,custom_ticks=None):
    geosource = GeoJSONDataSource(geojson = json_map_df)
    palette = bokeh.palettes.viridis(10)
    palette = palette[::-1]  
    # Map range of numbers to a colour palette
    color_mapper = LinearColorMapper(palette = palette, low=cbar_low_y, high=cbar_high_y)
    #Add a hover tooltip on final plot
    # expects a dictionary of hover fields items 
    fields_tuple = list(hover_fields.items())
    hover = HoverTool(tooltips = fields_tuple)
    if custom_ticks is not None:
        # create colour bar with custom tick labels if provided
        cbar_ticker = FixedTicker(ticks=custom_ticks)
    else:
        cbar_ticker=BasicTicker()
    #Create a colour bar with default tick labels
    color_bar = ColorBar(color_mapper=color_mapper,ticker=cbar_ticker,label_standoff=8,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal')
    # Start plotting!
    map_plot = figure(title = plot_title, plot_height = 700 , plot_width = 500, toolbar_location = None,tools=[hover])
    #p.add_tile(tile_provider)
    map_plot.xgrid.grid_line_color = None
    map_plot.ygrid.grid_line_color = None
    #Add patch renderer to figure.
    map_plot.patches('xs','ys', source = geosource,fill_color = {'field' :plotfield, 'transform' : color_mapper},
          line_color = 'black', line_width = 0.1, fill_alpha = .8)
    #Specify figure layout.
    map_plot.add_layout(color_bar, 'below')
    map_plot.xaxis.visible=False
    map_plot.yaxis.visible=False
    #Save the figure
    if(save_output):
        outfile_name="output/html/"+plot_title.title().replace(' ','')+".html"
        output_file(outfile_name)
        save(map_plot)
    else:
        show(map_plot)

    return map_plot

    

def setup_plots():
    print("Generating plots...")
    hover_fields_standard={'Area':'@Area','Average IMD':'@IMD','Cases':'@Cases','Date':'@Date'}
    hover_fields_imd_norm={'Area':'@Area','Normalised Average IMD':'@IMDNorm','Cases':'@Cases','Date':'@Date'}

    return hover_fields_standard, hover_fields_imd_norm
     
