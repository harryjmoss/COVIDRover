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

