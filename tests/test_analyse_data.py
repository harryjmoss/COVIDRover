import pandas as pd
import numpy as np
import os
from covidrover.analysis import analyse_data

def test_merging_by_areacode():
    covidInfoCols=['Area name', 'Area code', 'Area type',
     'Specimen date','Daily lab-confirmed cases',
      'Previously reported daily cases','Change in daily cases',
       'Cumulative lab-confirmed cases','Previously reported cumulative cases', 
       'Change in cumulative cases','Cumulative lab-confirmed cases rate']
    areaIMDCols=['Area code', 'IMD']
    covidInfo=pd.DataFrame(columns=covidInfoCols)
    areaIMDCols=pd.DataFrame(columns=areaIMDCols)

    merged=analyse_data.merge_by_area(covidInfo,areaIMDCols)
    assert len(merged.columns) == 12

def test_get_latest_date():
    csv_dataframe = pd.read_csv('data/csvText.csv') # test csv in data/
    latestdate='2020-06-17'
    csv_dataframe=csv_dataframe[csv_dataframe['Specimen date']==csv_dataframe['Specimen date'].max()]
    csv_dataframe=csv_dataframe.dropna(axis=1,how='all')
    csv_dataframe.index=np.arange(0,len(csv_dataframe))
    assert csv_dataframe['Specimen date'].all()==latestdate

