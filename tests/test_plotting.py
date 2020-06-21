from covidrover.plotting import plot_data
import numpy as np
import pandas as pd

def test_plot_2d_hist():
    test_title="title"
    test_xlabel="test_x"
    test_ylabel="test_y"
    test_xbins=np.arange(0,10,5)
    test_ybins=np.arange(0,10,5)
    random_vals=np.random.rand(1,2)
    test_dataframe=pd.DataFrame(random_vals,columns=[test_xlabel,test_ylabel])

   # this creates a png
    test_hist_arrays=plot_data.plot_2d_hist(test_dataframe,test_title,
                    test_xlabel,test_ylabel,test_xbins,test_ybins,write_file=False)
    assert len(test_hist_arrays) > 0

def test_plot_chloropleth():
    test_json={"type": "FeatureCollection", "features":
                [{"id": "0", "type": "Feature", 
                "properties": {"Area": "Hartlepool", "CRate": 377.5,
                "Cases": 352, "Code": "E06000001", "Date": "2020-06-19",
                "Deaths": 100.0, "IMD": 35.037, "IMDNorm": 0.7779257976420436,
                "MRate": "105.8", "MRateHighCI": "126.6", "MRateLowCI": "84.9",
                "testIMDLog": 0.8909381738386905}, 
                "geometry": {"type": "Polygon", "coordinates": [[[-1.26845558516825, 54.7261163520838]]]}
                }]}

    # Create a bokeh figure object
    plotfield='Cases'
    plot_title='test_plot'
    hover_fields={'Area':'@Area'}
    cbar_low_y=0
    cbar_high_y=3500

    test_plot=(test_json,plotfield,plot_title,hover_fields,cbar_low_y,cbar_high_y,False)
    # check it's not NoneType

    assert not isinstance(test_plot,type(None))


def test_geojson_generation():
    from bokeh.models import GeoJSONDataSource
    import json
    # pass this custom json
    test_dict={"type": "FeatureCollection", "features":
                [{"id": "0", "type": "Feature", 
                "properties": {"Area": "Hartlepool", "CRate": 377.5,
                "Cases": 352, "Code": "E06000001", "Date": "2020-06-19",
                "Deaths": 100.0, "IMD": 35.037, "IMDNorm": 0.7779257976420436,
                "MRate": "105.8", "MRateHighCI": "126.6", "MRateLowCI": "84.9",
                "testIMDLog": 0.8909381738386905}, 
                "geometry": {"type": "Polygon", "coordinates": [[[-1.26845558516825, 54.7261163520838]]]}
                }]}
    test_json = json.dumps(test_dict)
    test_geosource = GeoJSONDataSource(geojson = test_json)
    assert str(type(test_geosource)) == "<class 'bokeh.models.sources.GeoJSONDataSource'>"


def test_setup_plots():
    expected_fields={'Area':'@Area','Average IMD':'@IMD','Cases':'@Cases','Date':'@Date'}
    expected_fields_norm={'Area':'@Area','Normalised Average IMD':'@IMDNorm','Cases':'@Cases','Date':'@Date'}
    
    returned_fields,returned_fields_norm = plot_data.setup_plots()

    assert expected_fields == returned_fields
    assert expected_fields_norm == returned_fields_norm