import numpy as np
import pandas as pd
import geopandas as gpd
import requests, os
from io import StringIO
from .query_apis import run_api_query
import json

def get_latest_dataframes(json_out: list):
    # Get the latest available covid stats and read into pandas DataFrame
    dataframe = pd.read_json(json.dumps(json_out))
    return dataframe

def get_geo_data(geo_file):
    # geo_file can also be a url!
    geo_df=gpd.read_file(geo_file)
    return geo_df

def get_geomap_path(geopath,geo_url):
    if not(os.path.exists(geopath)):
        print("Getting geographical information...")
        geo_dataframe=get_geo_data(geo_url)
        geo_dataframe=geo_dataframe[['lad19cd','geometry']]
        geo_dataframe.columns=['code','geometry']  
        geo_dataframe.to_file(geopath)
    return geopath

def clean_deprivation_area_df(dep_df):
    dep_df=dep_df.iloc[:, : 3]
    dep_df.columns=['code',
    'name',
    'IMD']
    areaCodeList=dep_df['code'].str.rsplit(pat='/',n=1).tolist()
    areaCodeList=np.array(areaCodeList)
    areaCodeList=areaCodeList[:,-1]
    dep_df['code']=areaCodeList
    area_dep=dep_df[['code','IMD']]
    return area_dep
    
def prepare_data(geo_path,endpoint_url,deaths_imd_deciles):
    print("Preparing input data...")
    geography=get_geo_data(geo_path)
    updated_df = get_latest_dataframes(run_api_query(endpoint_url))

    deaths_imd=pd.read_csv(deaths_imd_deciles)
    local_area_deprivation="data/deprivation_index_by_area.csv"
    deprivation_df=pd.read_csv(local_area_deprivation)
    area_imd=clean_deprivation_area_df(deprivation_df)

    return geography, updated_df, area_imd, deaths_imd


