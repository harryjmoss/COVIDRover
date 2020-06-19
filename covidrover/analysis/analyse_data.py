import numpy as np
import pandas as pd
import datetime

def merge_by_area(covid,imd):
    return pd.merge(covid, imd, how='inner', on='Area code')


def analyse(cases,deaths,areaIMD):
    cases_area_IMD=merge_by_area(cases,areaIMD)
    print(cases_area_IMD)

