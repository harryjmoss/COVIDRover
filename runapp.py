import os
import sys
from covidrover import app
from covidrover import update_plots

sys.path.append(os.path.dirname(__name__))
# generate plots on the first run of the app...
#outfile_names=update_plots.main()

outfile_names =""

# run the app
app.main(outfile_names)
