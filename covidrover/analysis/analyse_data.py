import numpy as np
import pandas as pd
import json


def merge_by_area(leftdf,rightdf):
    # merges covid info dataframe with deprivation scores
    return pd.merge(leftdf, rightdf, how='inner', on='code')

def get_latest_data(merged_data):
    # Get the latest available data and only keep lower tier local authority entries
    latestcases=merged_data[merged_data['date']==merged_data['date'].max()]
    # Replace NaN values with zeros
    latestcases=latestcases.replace(np.nan,0.0)
    # Sort by averagedeprivation score
    latestcases=latestcases.sort_values(by='IMD') # sort by IMD score
    # Reset the index
    latestcases.index=np.arange(0,len(latestcases))
    latestcases['IMDNorm']=latestcases['IMD']/(latestcases['IMD'].max())
    # Reset column names for ease of use
    latestcases.columns=['Date','Area', 'Area code','New cases', 
                        'Total cases', 'Cases Per 100k', 'New deaths',
                        'Total deaths', 'Deaths Per 100k',
                        'IMD','IMDNorm']
    return latestcases

def convert_to_json_out(geodf):
    # Read geopandas dataframe in to json
    json_info = json.loads(geodf.to_json())
    #Convert to a string-like object
    json_out = json.dumps(json_info)
    return json_out

def analyse(mapdata, stats, area_imd):
    print("Analysing data...")
    # Get a combined dataframe with cases info and IMD score
    stats_area_imd=merge_by_area(stats,area_imd)
    # Get the latest available UK Gov COVID stats for England
    latest_stats_imd=get_latest_data(stats_area_imd)
    # Merge the cases and IMD data with geographic data  
    stats_imd_maps=merge_by_area(mapdata,latest_stats_imd)
    stats_imd_maps_json = convert_to_json_out(stats_imd_maps)
    return(stats_imd_maps, stats_imd_maps_json)
