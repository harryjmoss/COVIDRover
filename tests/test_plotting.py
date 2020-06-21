from covidrover.plotting import plot_data
import numpy as np
import pandas as pd

def test_plot_2d_hist():
    test_title="title"
    test_xlabel="test_x"
    test_ylabel="test_y"
    random_vals=np.random.rand(1,2)
    test_dataframe=pd.DataFrame(random_vals,columns=[test_xlabel,test_ylabel])

   # this creates a png
    test_hist_arrays=plot_data.plot_2d_hist(test_dataframe,test_title,
                    test_xlabel,test_ylabel,10,write_file=False)
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

    # this creates a bokeh figure object
    # check it's not NoneType
    plotfield='Cases'
    plot_title='test_plot'
    hover_fields={'Area':'@Area'}
    cbar_low_y=0
    cbar_high_y=3500


    test_plot=(test_json,plotfield,plot_title,hover_fields,cbar_low_y,cbar_high_y,False)
    assert not isinstance(test_plot,type(None))
