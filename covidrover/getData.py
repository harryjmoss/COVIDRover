import pandas as pd
import requests
from io import StringIO

def download_latest_csvs(cases_url, deaths_url):
    caseCSV=requests.get(cases_url).text
    caseDF=pd.read_csv(StringIO(caseCSV))
    deathCSV=requests.get(deaths_url).text
    deathDF=pd.read_csv(StringIO(deathCSV))
    return caseDF, deathDF

def main():
    cases_url = "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv"
    deaths_url = "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-deaths_latest.csv"

    casesDF, deathsDF = download_latest_csvs(cases_url, deaths_url)

    print(deathsDF)

if __name__ == '__main__':
    main()

