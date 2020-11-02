"""Analyse data collected, remove NaN values, get the latest data"""
import numpy as np
import pandas as pd


def merge_by_area(leftdf: pd.DataFrame, rightdf: pd.DataFrame) -> pd.DataFrame:
    """Merges covid info dataframe with deprivation scores"""

    return pd.merge(leftdf, rightdf, how="inner", on="Area code")


def get_latest_data(merged_data: pd.DataFrame) -> pd.DataFrame:
    """Get latest available data, calculate variables
    and rename fields
    """
    # Get the latest available data
    latestcases = merged_data[merged_data["date"] == merged_data["date"].max()]
    # Replace NaN values with zeros
    latestcases = latestcases.replace(np.nan, 0.0)
    # Sort by averagedeprivation score
    latestcases = latestcases.sort_values(by="IMD")  # sort by IMD score
    # Reset the index
    latestcases.index = np.arange(0, len(latestcases))
    latestcases["IMDNorm"] = latestcases["IMD"] / (latestcases["IMD"].max())
    # Reset column names for ease of use
    latestcases.columns = [
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
    return latestcases


def convert_to_json_out(geodf: pd.DataFrame) -> str:
    """Read geopandas dataframe in to json"""
    # Convert datetime object to str for json serialization
    geodf["Date"] = geodf["Date"].astype(str)
    json_out = geodf.to_json()
    return json_out


def analyse(mapdata, stats, area_imd):
    """Main data analysis function"""
    print("Analysing data...")
    # Get a combined dataframe with cases info and IMD score
    stats_area_imd = merge_by_area(stats, area_imd)
    # Get the latest available UK Gov COVID stats for England
    latest_stats_imd = get_latest_data(stats_area_imd)
    # Merge the cases and IMD data with geographic data
    stats_imd_maps = merge_by_area(mapdata, latest_stats_imd)
    stats_imd_maps_json = convert_to_json_out(stats_imd_maps)
    return (stats_imd_maps, stats_imd_maps_json)
