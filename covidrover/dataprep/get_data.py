"""Module to collect data - run an API query, load data into pandas dataframes
and set column names.
"""
import json
import os
from typing import List, Dict
import numpy as np
import pandas as pd
import geopandas as gpd
from .query_apis import run_api_query


def get_latest_dataframes(json_out: list) -> pd.DataFrame:
    """Get the latest available covid stats and read into pandas DataFrame"""
    dataframe = pd.read_json(json.dumps(json_out))
    dataframe.columns = [
        "date",
        "name",
        "Area code",
        "daily",
        "cumulative",
        "caseRate",
        "newDeaths",
        "cDeaths",
        "deathRate",
    ]
    return dataframe


def get_geo_data(geo_file: str) -> gpd.GeoDataFrame:
    """Get the geographical file (can be a URL)"""
    geo_df = gpd.read_file(geo_file)
    return geo_df


def get_geomap_path(geopath: str, geo_url: str) -> str:
    """Get geographical information from a path"""
    if not os.path.exists(geopath):
        print("Getting geographical information...")
        geo_dataframe = get_geo_data(geo_url)
        geo_dataframe = geo_dataframe[["lad19cd", "geometry"]]
        geo_dataframe.columns = ["code", "geometry"]
        geo_dataframe.to_file(geopath)
    return geopath


def clean_deprivation_area_df(dep_df: pd.DataFrame) -> pd.DataFrame:
    """Refactor IMD data in pandas dataframe"""
    dep_df = dep_df.iloc[:, :3]
    dep_df.columns = ["Area code", "name", "IMD"]
    area_code_list = dep_df["Area code"].str.rsplit(pat="/", n=1).tolist()
    area_code_list = np.array(area_code_list)
    area_code_list = area_code_list[:, -1]
    dep_df["Area code"] = area_code_list
    area_dep = dep_df[["Area code", "IMD"]]
    return area_dep


def prepare_data(geo_path, endpoint_url, deaths_imd_deciles):
    """Prepare all input data"""
    print("Preparing input data...")
    geography = get_geo_data(geo_path)
    query_filters: List = ["areaType=ltla"]
    query_structure: Dict = {
        "date": "date",
        "name": "areaName",
        "code": "areaCode",
        "daily": "newCasesBySpecimenDate",
        "cumulative": "cumCasesBySpecimenDate",
        "caseRate": "cumCasesBySpecimenDateRate",
        "newDeaths": "newDeaths28DaysByDeathDate",
        "cDeaths": "cumDeaths28DaysByDeathDate",
        "deathRate": "cumDeaths28DaysByDeathDateRate",
    }
    updated_df = get_latest_dataframes(
        run_api_query(endpoint_url, query_filters, query_structure)
    )

    deaths_imd = pd.read_csv(deaths_imd_deciles)
    local_area_deprivation = "data/deprivation_index_by_area.csv"
    deprivation_df = pd.read_csv(local_area_deprivation)
    area_imd = clean_deprivation_area_df(deprivation_df)

    return geography, updated_df, area_imd, deaths_imd
