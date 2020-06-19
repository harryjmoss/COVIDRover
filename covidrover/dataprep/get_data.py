import numpy as np
import pandas as pd
import requests
from io import StringIO

def download_latest_csvs(csvurl):
    csvtext=requests.get(csvurl).text
    csvDF=pd.read_csv(StringIO(csvtext))
    return csvDF

def clean_deprivation_area_df(depDF):
    depDF=depDF.iloc[:, : 3]
    depDF.columns=['Area code',
    'Reference area',
    'IMD']
    areaCodeList=depDF['Area code'].str.rsplit(pat='/',n=1).to_list()
    areaCodeList=np.array(areaCodeList)
    areaCodeList=areaCodeList[:,-1]
    depDF['Area code']=areaCodeList
    areaIMD=depDF[['Area code','IMD']]
    return areaIMD
def prepare_data(cases_url,deaths_url):
    cases=download_latest_csvs(cases_url)
    deaths=download_latest_csvs(deaths_url)

    local_area_deprivation="data/deprivation_index_by_area.csv"
    deprivationDF=pd.read_csv(local_area_deprivation)
    areaIMD=clean_deprivation_area_df(deprivationDF)

    return cases, deaths, areaIMD


