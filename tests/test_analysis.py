import pandas as pd
import numpy as np
from covidrover.analysis import analyse_data
from datetime import datetime


def test_merge_by_area():
    covidInfoCols = [
        "Area name",
        "Area code",
        "Area type",
        "Specimen date",
        "Daily lab-confirmed cases",
        "Previously reported daily cases",
        "Change in daily cases",
        "Cumulative lab-confirmed cases",
        "Previously reported cumulative cases",
        "Change in cumulative cases",
        "Cumulative lab-confirmed cases rate",
    ]
    areaIMDCols = ["Area code", "IMD"]
    covidInfo = pd.DataFrame(columns=covidInfoCols)
    areaIMDCols = pd.DataFrame(columns=areaIMDCols)

    merged = analyse_data.merge_by_area(covidInfo, areaIMDCols)
    assert len(merged.columns) == 12


def test_get_latest_date():
    csv_dataframe = pd.read_csv("tests/inputs/csvText.csv")  # test csv in data/
    latestdate = "2020-06-17"
    csv_dataframe = csv_dataframe[
        csv_dataframe["Specimen date"] == csv_dataframe["Specimen date"].max()
    ]
    csv_dataframe = csv_dataframe.dropna(axis=1, how="all")
    csv_dataframe.index = np.arange(0, len(csv_dataframe))
    assert csv_dataframe["Specimen date"].all() == latestdate


def test_get_latest_data():
    test_columns = [
        "date",
        "Area",
        "Area code",
        "Cases",
        "CasesTotal",
        "CasesRate",
        "Deaths",
        "Total deaths",
        "Deaths rate",
        "IMD",
        "IMDNorm",
    ]
    test_list = [
        [
            "2020-06-19",
            "Hart",
            "E07000089",
            200,
            300,
            0.5,
            186,
            195,
            3.0,
            5.544,
            0.005,
        ],
        [
            "2020-09-19",
            "Hart",
            "E07000089",
            200,
            800,
            0.5,
            186,
            300,
            3.0,
            5.544,
            0.005,
        ],
    ]

    test_dataframe = pd.DataFrame(test_list, columns=test_columns)
    test_new_dataframe = analyse_data.get_latest_data(test_dataframe)
    expected_columns = [
        "Date",
        "Area",
        "Area code",
        "NewCases",
        "TotalCases",
        "CasesPer100k",
        "NewDeaths",
        "TotalDeaths",
        "DeathsPer100k",
        "IMD",
        "IMDNorm",
    ]
    assert test_new_dataframe.columns.tolist() == expected_columns


def test_convert_to_json_out():
    test_array = np.array(
        [
            [
                "geometry",
                datetime.strptime("2020-06-19", "%Y-%m-%d"),
                "Hartlepool",
                "E00000",
                352.0,
                400,
                0.5,
                377.5,
                400,
                1.5,
                35.037,
                0.7,
            ],
            [
                "geometry",
                datetime.strptime("2020-06-19", "%Y-%m-%d"),
                "Middlesbrough",
                "E000001",
                352.0,
                400,
                0.5,
                377.5,
                400,
                1.5,
                35.037,
                0.7,
            ],
            [
                "geometry",
                datetime.strptime("2020-06-19", "%Y-%m-%d"),
                "Redcar and Cleveland",
                695.0,
                494.5,
                40.46,
            ],
        ]
    ).tolist()
    columns_list = [
        "Geography",
        "Date",
        "Area",
        "Area code",
        "NewCases",
        "TotalCases",
        "CasesPer100k",
        "NewDeaths",
        "TotalDeaths",
        "DeathsPer100k",
        "IMD",
        "IMDNorm",
    ]
    test_dataframe = pd.DataFrame(test_array, columns=columns_list)
    test_jsoninfo = analyse_data.convert_to_json_out(test_dataframe)
    assert isinstance(test_jsoninfo, str)
