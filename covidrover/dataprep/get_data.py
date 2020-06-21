import numpy as np
import pandas as pd
import geopandas as gpd
import requests, sys, fiona
from io import StringIO

def get_latest_dataframes(requrl):
    # Get the latest available covid stats file and read into pandas DataFrame
    csvtext=requests.get(requrl).text
    dataframe=pd.read_csv(StringIO(csvtext))
    return dataframe

def get_geo_data(geo_file):
    geo_df=gpd.read_file(geo_file)
    return geo_df


def clean_deprivation_area_df(dep_df):
    dep_df=dep_df.iloc[:, : 3]
    dep_df.columns=['Area code',
    'Reference area',
    'IMD']
    areaCodeList=dep_df['Area code'].str.rsplit(pat='/',n=1).tolist()
    areaCodeList=np.array(areaCodeList)
    areaCodeList=areaCodeList[:,-1]
    dep_df['Area code']=areaCodeList
    area_dep=dep_df[['Area code','IMD']]
    return area_dep
    
def prepare_data(geo_path,cases_url,deaths_url,deaths_imd_deciles):
    print("Preparing input data...")
    geography=get_geo_data(geo_path)
    cases=get_latest_dataframes(cases_url)
    deaths=get_latest_dataframes(deaths_url)
    deaths_imd=pd.read_csv(deaths_imd_deciles)

    local_area_deprivation="data/deprivation_index_by_area.csv"
    deprivation_df=pd.read_csv(local_area_deprivation)
    area_imd=clean_deprivation_area_df(deprivation_df)

    return geography, cases, deaths, area_imd, deaths_imd


