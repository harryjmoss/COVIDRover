from dataprep import get_data
from analysis import analyse_data
def main():
    cases_url = "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv"
    deaths_url = "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-deaths_latest.csv"
    
    cases, deaths, areaIMD = get_data.prepare_data(cases_url,deaths_url)
    analyse_data.analyse(cases,deaths,areaIMD)

    
    print("Run!")

if __name__ == '__main__':
    main()
