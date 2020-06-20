import numpy as np
import pandas as pd
import datetime

def merge_by_area(covid,imd):
    # merges covid info dataframe with deprivation scores
    return pd.merge(covid, imd, how='inner', on='Area code')

def get_latest_data(merged_data):
    # get the latest data
    latestcases=merged_data[(merged_data['Specimen date']==merged_data['Specimen date'].max())
                             & (merged_data['Area type'].str.match('Lower tier local authority'))]
    latestcases=latestcases.dropna(axis=1,how='all') # remove all columns that are all NaN
    latestcases=latestcases.sort_values(by='IMD') # sort by IMD score
    latestcases.index=np.arange(0,len(latestcases))
    return latestcases

def analyse(map,cases,deaths,area_imd):
    print("Analysing data...")
    cases_area_imd=merge_by_area(cases,area_imd)
    latestcases_imd=get_latest_data(cases_area_imd)
    print(latestcases_imd)
    

