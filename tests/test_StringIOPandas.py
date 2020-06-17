# test_csv_to_dataframe
import pandas as pd

def generate_dataframe_from_csv(testcsv):
    df = pd.read_csv(testcsv)
    return df

def test_generate_dataframe_from_csv():
    df = generate_dataframe_from_csv('data/csvText.csv')
    expected_columns = ["Area name","Area code","Area type",
                        "Specimen date","Daily lab-confirmed cases",
                        "Previously reported daily cases","Change in daily cases",
                        "Cumulative lab-confirmed cases","Previously reported cumulative cases",
                        "Change in cumulative cases","Cumulative lab-confirmed cases rate"]
    assert df.columns.tolist()  == expected_columns
