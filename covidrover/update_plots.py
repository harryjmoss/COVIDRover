from covidrover.dataprep import get_data
from covidrover.analysis import analyse_data
from covidrover.plotting import plot_data
from covidrover import setup
import numpy as np
import time
def main():
    start_timer = time.time()
    # This file is retrieved in setup.py and saved to the data directory if it does not already exist
    geomap_path=setup.get_geomap_path()
    # UK Gov covid cases data:
    cases_url = "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv"
    # UK Gov covid deaths data:
    deaths_url = "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-deaths_latest.csv"
   
    # England & Wales mortality statistics by deprivation decile between March and May 2020
    marmay_deaths_imd_deciles = "data/deaths_by_gender_deprivationDecile.csv"
    
    # Get the data
    map_df, cases, deaths, areaIMD, deaths_imd = get_data.prepare_data(geomap_path,cases_url,deaths_url,marmay_deaths_imd_deciles)
    # Prepare the data, combine and calculate variables to plot
    stats_maps,stats_maps_json= analyse_data.analyse(map_df,cases,deaths,areaIMD)
    
    # Plot the data!
    # Sets up the hover fields for the chloropleth map plots
    hover_fields,hover_fields_norm =plot_data.setup_plots()

    xbins=np.arange(0,55,5)
    ybins=np.arange(0,4000,500)
    title_hist2d = "Frequency of case numbers as a function of IMD"
    histarrays=plot_data.plot_2d_hist(stats_maps,title_hist2d,'IMD','Cases',xbins,ybins)


    cases_area_plot=plot_data.plot_chloropleth(stats_maps_json,'Cases','Lab-Confirmed COVID-19 Cases By Area in England',hover_fields,0,3500,True)
    imd_area_plot=plot_data.plot_chloropleth(stats_maps_json,'IMD','Average Index of Multiple Deprivation By Lower Tier Local Authority in England',hover_fields,0,50,True,)
    imd_norm_area_plot=plot_data.plot_chloropleth(stats_maps_json,'IMDNorm','Normalised Average Index of Multiple Deprivation By Lower Tier Local Authority in England',hover_fields_norm,0,1,True)

    deaths_decile_imd_title="COVID-19 Mortality per 100000 People by Deprivation Decile between March and May 2020"
    deaths_decile_imd_xaxis_label="COVID-19 mortality rate per 100000 people (2018 pop. estimate)"
    deaths_decile_imd_yaxis_label="Deprivation decile (1: most deprived, 10: least deprived)"
    deaths_decile_plot=plot_data.plot_deaths_imd_decile(deaths_imd,deaths_decile_imd_title,deaths_decile_imd_xaxis_label,deaths_decile_imd_yaxis_label)

    print("--- Finished running in %s seconds ---" % (time.time() - start_timer))
    return
if __name__ == '__main__':
    main()
