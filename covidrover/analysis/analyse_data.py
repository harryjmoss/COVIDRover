import numpy as np
import pandas as pd
import json


def merge_by_area(leftdf,rightdf):
    # merges covid info dataframe with deprivation scores
    return pd.merge(leftdf, rightdf, how='inner', on='Area code')

def get_latest_data(merged_data):
    # Get the latest available data and only keep lower tier local authority entries
    latestcases=merged_data[(merged_data['Specimen date']==merged_data['Specimen date'].max())
                             & (merged_data['Area type'].str.match('Lower tier local authority'))]
    # Drop columns not needed
    latestcases=latestcases.drop(columns=['Area type','Daily lab-confirmed cases'])
    # Drop columns filled with NaN values
    latestcases=latestcases.dropna(axis=1,how='all') # remove all columns that are all NaN
    # Sort by averagedeprivation score
    latestcases=latestcases.sort_values(by='IMD') # sort by IMD score
    # Reset the index
    latestcases.index=np.arange(0,len(latestcases))
    latestcases['IMDNorm']=latestcases['IMD']/(latestcases['IMD'].max())
    # Reset column names for ease of use
    latestcases.columns=['Area', 'Area code', 
                        'Date','Cases',
                        'RatePer100k','IMD','IMDNorm']
    return latestcases

def convert_to_json_out(geodf):
    # Read geopandas dataframe in to json
    json_info = json.loads(geodf.to_json())
    #Convert to a string-like object
    json_out = json.dumps(json_info)
    return json_out

def analyse(mapdata,cases,deaths,area_imd):
    print("Analysing data...")
    # Get a combined dataframe with cases info and IMD score
    cases_area_imd=merge_by_area(cases,area_imd)
    # Get the latest available UK Gov COVID stats for England
    latestcases_imd=get_latest_data(cases_area_imd)
    # Merge the cases and IMD data with geographic data  
    cases_imd_maps=merge_by_area(mapdata,latestcases_imd)
    cases_imd_maps_json = convert_to_json_out(cases_imd_maps)
    return(cases_imd_maps,cases_imd_maps_json)
