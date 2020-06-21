# test_dataprep
import pandas as pd
import numpy as np
import geopandas, os, requests, pytest
from covidrover.dataprep import get_data

class TestRequests():
    testurl_200="https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv"
    testurl_404="https://github.com/404"
    @pytest.mark.parametrize("input,expected", [
        (testurl_200, 200),
        (testurl_404, 404),
    ])
    
    def test_request(self,input,expected):
        csvtext=requests.get(input)
        assert csvtext.status_code == expected

class TestFilesExist():
    test_deprivationdata='data/deprivation_index_by_area.csv'
    test_textcsv='tests/inputs/csvText.csv'
    test_deaths_gender_deprivationdecile='data/deaths_by_gender_deprivationDecile.csv'
    test_deaths_regions='data/mortality_stats_byArea_EnglandWales_MarchMay2020.csv'

    @pytest.mark.parametrize("input", [
        (test_deprivationdata),
        (test_textcsv),
        (test_deaths_gender_deprivationdecile),
        (test_deaths_regions)
    ])
    def test_file_exists(self,input): 
        assert os.path.exists(input)

class TestDataFames():

    def generate_dataframe_from_csv(self,testcsv):
        dataframe = pd.read_csv(testcsv)
        return dataframe


    def test_generate_dataframe_from_csv(self):
        df = self.generate_dataframe_from_csv('tests/inputs/csvText.csv')
        expected_columns = ["Area name","Area code","Area type",
                        "Specimen date","Daily lab-confirmed cases",
                        "Previously reported daily cases","Change in daily cases",
                        "Cumulative lab-confirmed cases","Previously reported cumulative cases",
                        "Change in cumulative cases","Cumulative lab-confirmed cases rate"]
        assert df.columns.tolist()  == expected_columns

    def test_get_latest_dataframes(self):
        # use deaths url, file is much smaller
        deaths_url="https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv"
        test_dataframe=get_data.get_latest_dataframes(deaths_url)
        assert not test_dataframe.empty

    def test_clean_deprivation_area_df(self):
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
        'j. Income Deprivation Affecting Older People Index (IDAOPI)'
        ]

        vals=["http://opendatacommunities.org/id/geography/administration/ua/E06000022",
        "Bath and North East Somerset" ,11.745,0.079,0.063,14.043,-0.668,-0.279,16.763,
        13.986,0.104,0.096]
        testdataframe=pd.DataFrame([vals],columns=inputcolumns)
        expectedcolumns = ['Area code','IMD']
        cleanedcolumns=get_data.clean_deprivation_area_df(testdataframe).columns.to_list()
        assert cleanedcolumns == expectedcolumns

class TestGeoDataFrames():
    test_geo_file='tests/inputs/test_geo.shp'
    test_fake_path='tests/inputs/test_fake_geo.shp'    
    # from an arcGIS json request for the liverpool area code
    test_liverpool_json='tests/inputs/test_geo_json.json'
    def test_get_geo_file_exists(self):
        assert os.path.exists(self.test_geo_file)
    
    def test_get_geo_data(self):
        test_geo_df=get_data.get_geo_data(self.test_geo_file)
        assert isinstance(test_geo_df,geopandas.geodataframe.GeoDataFrame)

    def test_get_geomap_path(self):
        output_geo_path=get_data.get_geomap_path(self.test_fake_path,self.test_liverpool_json)
        assert os.path.exists(output_geo_path)
        fake_path_base = output_geo_path.rsplit('.',1)[0]
        fake_path_ext =output_geo_path.rsplit('.',1)[1]
        if (fake_path_ext == "shp"):
            # will create extra files
            for ext in [".cpg",".prj",".dbf",".shx"]:
                os.remove(fake_path_base+ext)
        os.remove(output_geo_path)


    

    
