# test_csv_to_dataframe
import pandas as pd
import os

def generate_dataframe_from_csv(testcsv):
    df = pd.read_csv(testcsv)
    return df

def file_exists(testfile): 
    return os.path.exists(testfile)

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