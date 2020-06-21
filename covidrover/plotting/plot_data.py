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
    # sorts out padding, just aesthetic
    plt.tight_layout()

    if(write_file):
        output_file_name = "output/png/"+hist_title.title().replace(' ','')+".png"
        plt.savefig(output_file_name,dpi=300)
    return two_dim_hist

def plot_deaths_imd_decile(deaths_imd,hist_title,xaxis_label,yaxis_label,write_file=True):
    # Sort the dataframe into All, Women, Men
    deaths_imd_all=deaths_imd[deaths_imd['Sex'].str.match('Persons')].drop(columns="Sex")
    deaths_imd_men=deaths_imd[deaths_imd['Sex'].str.match('Males')].drop(columns="Sex")
    deaths_imd_women=deaths_imd[deaths_imd['Sex'].str.match('Females')].drop(columns="Sex")

    # set up figure and axis
    plt.figure(None,[10,8]) # figure number, [width,height (inches)]
    ax=plt.gca()
    
    # Plot the lines of the mean fatality rate for All people, women and men
    # Also plot the 95% CI error band around the mean
    # Blank/filled labels for the bands is just stylistic
    plt.plot(deaths_imd_all['Decile'].tolist(),deaths_imd_all['Rate'].tolist(),"Green",label='All')
    plt.fill_between(deaths_imd_all['Decile'].tolist(),deaths_imd_all['LowerCI'],deaths_imd_all['UpperCI'],color="Green",alpha=0.5,label=" ")
    plt.plot(deaths_imd_women['Decile'].tolist(),deaths_imd_women['Rate'].tolist(),"Orange",label='Women')
    plt.fill_between(deaths_imd_women['Decile'].tolist(),deaths_imd_women['LowerCI'],deaths_imd_women['UpperCI'],color="Orange",alpha=0.5,label="95% CI")
    plt.plot(deaths_imd_men['Decile'].tolist(),deaths_imd_men['Rate'].tolist(),"Red",label='Men')
    plt.fill_between(deaths_imd_men['Decile'].tolist(),deaths_imd_men['LowerCI'],deaths_imd_men['UpperCI'],color="Red",alpha=0.5,label=" ")

    # set title, ticks, labels
    plt.title(hist_title)
    ax.set_ylabel(xaxis_label)
    ax.set_xlabel(yaxis_label)
    ax.set_xticks(np.arange(0,11))
    plt.legend(loc="upper right")

    output_file_name = "output/png/"+hist_title.title().replace(' ','')+".png"
    # write file, or don't 
    if(write_file):
        plt.savefig(output_file_name,dpi=300)
    return output_file_name

def plot_chloropleth(json_map_df,plotfield,plot_title,hover_fields,cbar_low_y,cbar_high_y,save_output=True,custom_ticks=None):
    geosource = GeoJSONDataSource(geojson = json_map_df)
    if custom_ticks is not None:
        # create colour bar with custom tick labels if provided
        cbar_ticker = FixedTicker(ticks=custom_ticks)
        palette = bokeh.palettes.viridis(len(custom_ticks))
    else:
        cbar_ticker=BasicTicker()
        palette = bokeh.palettes.viridis(10)
    palette = palette[::-1]  
    # Map range of numbers to a colour palette
    color_mapper = LinearColorMapper(palette = palette, low=cbar_low_y, high=cbar_high_y)
    #Add a hover tooltip on final plot
    # expects a dictionary of hover fields items 
    fields_tuple = list(hover_fields.items())
    hover = HoverTool(tooltips = fields_tuple)
    
        
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
     
