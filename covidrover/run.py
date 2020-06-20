from covidrover.dataprep import get_data
from covidrover.analysis import analyse_data
from covidrover import setup
def main():
    # This file is retrieved in setup.py and saved to the data directory if it does not already exist
    geomap_path=setup.get_geomap_path()
    # UK Gov covid cases data:
    cases_url = "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv"
    # UK Gov covid deaths data:
    deaths_url = "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-deaths_latest.csv"
   
    map_df, cases, deaths, areaIMD = get_data.prepare_data(geomap_path,cases_url,deaths_url)
    analyse_data.analyse(map_df,cases,deaths,areaIMD)

    
    print("Run!")

if __name__ == '__main__':
    main()
