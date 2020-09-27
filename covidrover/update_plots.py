from covidrover.dataprep import get_data
from covidrover.analysis import analyse_data
from covidrover.plotting import plot_data
import numpy as np
import time


def run_covidrover():
    start_timer = time.time()
    # This file is retrieved in plot_data and saved to the data directory if it does not already exist
    geopath = "data/geofiles/geofile.shp"
    geo_url = "https://opendata.arcgis.com/datasets/a8531598f29f44e7ad455abb6bf59c60_0.geojson"
    geomap_path = get_data.get_geomap_path(geopath, geo_url)

    # UK Gov covid data:
    endpoint_url = "https://api.coronavirus.data.gov.uk/v1/data"

    # England & Wales mortality statistics by deprivation decile between March and May 2020
    marmay_deaths_imd_deciles = "data/deaths_by_gender_deprivationDecile.csv"

    # Get the data
    map_df, stats, areaIMD, deaths_imd = get_data.prepare_data(
        geomap_path, endpoint_url, marmay_deaths_imd_deciles
    )
    # Prepare the data, combine and calculate variables to plot
    stats_maps, stats_maps_json = analyse_data.analyse(map_df, stats, areaIMD)

    # Plot the data!
    # Sets up the hover fields for the chloropleth map plots
    hover_fields, hover_fields_norm = plot_data.setup_plots()

    xbins = np.arange(0, 55, 5)
    ybins = np.arange(0, 4000, 500)
    title_hist2d = "Frequency of case numbers as a function of IMD"
    histarrays = plot_data.plot_2d_hist(
        stats_maps, title_hist2d, "IMD", "TotalCases", xbins, ybins
    )

    cases_area_plot = plot_data.plot_chloropleth(
        stats_maps_json,
        "TotalCases",
        "Positive COVID-19 PCR tests By Area in England by specimen date",
        hover_fields,
        0,
        4000,
        True,
        custom_ticks=np.arange(0, 12000, 1000),
    )
    case_rate_plot = plot_data.plot_chloropleth(
        stats_maps_json,
        "CasesPer100k",
        "Positive COVID-19 PCR tests By Area in England by specimen date per 100k",
        hover_fields,
        0,
        2000,
        True,
        custom_ticks=np.arange(0, 2000, 250),
    )
    deaths_area_plot = plot_data.plot_chloropleth(
        stats_maps_json,
        "TotalDeaths",
        "Deaths within 28 days of positive test by date of death",
        hover_fields,
        0,
        1200,
        True,
        custom_ticks=np.arange(0, 1200, 100),
    )
    death_rate_plot = plot_data.plot_chloropleth(
        stats_maps_json,
        "DeathsPer100k",
        "Deaths within 28 days of positive test by date of death per 100k",
        hover_fields,
        0,
        200,
        True,
        custom_ticks=np.arange(0, 200, 25),
    )
    imd_area_plot = plot_data.plot_chloropleth(
        stats_maps_json,
        "IMD",
        "Average Index of Multiple Deprivation By Lower Tier Local Authority in England",
        hover_fields,
        0,
        50,
        True,
    )
    imd_norm_area_plot = plot_data.plot_chloropleth(
        stats_maps_json,
        "IMDNorm",
        "Normalised Average Index of Multiple Deprivation By Lower Tier Local Authority in England",
        hover_fields_norm,
        0,
        1,
        True,
    )

    deaths_decile_imd_title = "COVID-19 Mortality per 100000 People by Deprivation Decile between March and May 2020"
    deaths_decile_imd_xaxis_label = (
        "COVID-19 mortality rate per 100000 people (2018 pop. estimate)"
    )
    deaths_decile_imd_yaxis_label = (
        "Deprivation decile (1: most deprived, 10: least deprived)"
    )
    deaths_decile_plot = plot_data.plot_deaths_imd_decile(
        deaths_imd,
        deaths_decile_imd_title,
        deaths_decile_imd_xaxis_label,
        deaths_decile_imd_yaxis_label,
    )

    bokehfiles = [
        cases_area_plot,
        case_rate_plot,
        deaths_area_plot,
        death_rate_plot,
        imd_area_plot,
        imd_norm_area_plot,
    ]

    imgfiles = {"2D_Hist": histarrays, "Deaths_Decile": deaths_decile_plot}
    print("--- Finished running in %s seconds ---" % (time.time() - start_timer))
    return bokehfiles, imgfiles


if __name__ == "__main__":
    run_covidrover()
