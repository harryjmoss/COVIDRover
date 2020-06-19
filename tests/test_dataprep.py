# test_dataprep
import pandas as pd
import os
import requests
from covidrover.dataprep import get_data

def make_csv_request(testurl):
    csvtext=requests.get(testurl)
    return csvtext.status_code

def generate_dataframe_from_csv(testcsv):
    df = pd.read_csv(testcsv)
    return df

def file_exists(testfile): 
    return os.path.exists(testfile)

def test_successful_request():
    testurl="https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv"
    assert make_csv_request(testurl) == 200

def test_generate_dataframe_from_csv():
    df = generate_dataframe_from_csv('data/csvText.csv')
    expected_columns = ["Area name","Area code","Area type",
                        "Specimen date","Daily lab-confirmed cases",
                        "Previously reported daily cases","Change in daily cases",
                        "Cumulative lab-confirmed cases","Previously reported cumulative cases",
                        "Change in cumulative cases","Cumulative lab-confirmed cases rate"]
    assert df.columns.tolist()  == expected_columns

def test_file_exists_areadeprivation():
    testfile="data/deprivation_index_by_area.csv"
    assert file_exists(testfile)

def test_dataframe_cleaning():
    inputcolumns=['http://opendatacommunities.org/def/ontology/geography/refArea',
        'Reference area',
        'a. Index of Multiple Deprivation (IMD)',
        'b. Income Deprivation Domain',
        'c. Employment Deprivation Domain',
        'd. Education, Skills and Training Domain',
        'e. Health Deprivation and Disability Domain',
        'f. Crime Domain',
        'g. Barriers to Housing and Services Domain',
        'h. Living Environment Deprivation Domain',
        'i. Income Deprivation Affecting Children Index (IDACI)',
        'j. Income Deprivation Affecting Older People Index (IDAOPI)']

    vals=["http://opendatacommunities.org/id/geography/administration/ua/E06000022",
    "Bath and North East Somerset" ,11.745,0.079,0.063,14.043,-0.668,-0.279,16.763,
    13.986,0.104,0.096]
    testdataframe=pd.DataFrame([vals],columns=inputcolumns)
    expectedcolumns = ['Area code','IMD']
    cleanedcolumns=get_data.clean_deprivation_area_df(testdataframe).columns.to_list()
    assert cleanedcolumns == expectedcolumns
