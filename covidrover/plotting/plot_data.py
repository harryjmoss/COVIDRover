import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import numpy as np


def plot_2d_hist(geodataframe,hist_title,xvar,yvar,nbins,mincases=1,write_file=True):
    # set up figure and axis objects    
    plt.figure()
    ax=plt.gca()
    # Creates a right-hand axis with fractional size of ax and with fixed padding
    plt.figure(1)
    ax=plt.gca()
    # get numpy arrays out of dataframe
    xdata = geodataframe[xvar].to_numpy()
    ydata = geodataframe[yvar].to_numpy()
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
        output_file_name = "output/"+hist_title.title().replace(' ','')+".png"
        plt.savefig(output_file_name)
    return two_dim_hist

def get_plots(stats_maps,stats_maps_json):
    print("Generating plots...")
    # plot an n * n bin 2d histogram with variables of your choice:
    title_string="Frequency of case numbers as a function of IMD"
    histarrays=plot_2d_hist(stats_maps,title_string,'IMD','Cases',10)
    
    return

