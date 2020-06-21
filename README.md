[![Build Status](https://travis-ci.org/harryjmoss/COVIDRover.svg?branch=master)](https://travis-ci.org/harryjmoss/COVIDRover)
# COVIDRover - a COVID-19 data analysis tool

A Python tool to query the latest available statistics on COVID-19 cases in the UK and perform analysis based on geographical and area deprivation information.

### Data sources
- COVID deaths and cases statistics are taken from https://coronavirus.data.gov.uk/ - licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)
- Deprivation index data is taken from the UK Ministry of Housing, Communities & Local Government and is available via [https://opendatacommunities.org/](https://opendatacommunities.org/resource?uri=http%3A%2F%2Fopendatacommunities.org%2Fdata%2Fsocietal-wellbeing%2Fimd2019%2Findices) under the Open Government Licence v3.0
- [Population data](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationprojections/datasets/localauthoritiesinenglandtable2) Source: Office for National Statistics (ONS) licensed under the Open Government Licence v3.0
- [Geographical data](https://hub.arcgis.com/datasets/a8531598f29f44e7ad455abb6bf59c60_0) Source: Office for National Statistics licensed under the Open Government Licence v.3.0

'Deprivation' is derived from the 'Index of multiple deprivation' (IMD) and is comprised of multiple factors. IMD in England is defined within [this document](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/853811/IoD2019_FAQ_v4.pdf). The definition used in this analysis is a population-weighted average of the combined scores of the smaller areas that comprise each region considered. 'IMD' in this context refers to this averaged score.

UK COVID-19 case and death numbers are requested from [https://coronavirus.data.gov.uk/](https://coronavirus.data.gov.uk/) on each run to provide the latest figures. Other datasets measure relevant statistics over the period of March &ndash; May 2020 where information with (almost) daily updates is not required or available.

## Setup
Install dependent packages with:  
`pip install -r requirements.txt`

The first time the program runs, geographical data is collected as a geoJSON file from the ONS Open Geography Portal if it does not exist in the `data` directory. The geoJSON is trimmed down and saved as a geoJSON file in the the `data` directory for future use. As the file is quite large(!), this (should) only happen the first time you run the package.

## Running
The package can be run from the base directory (containing this README) with  
`python run.py`
You can also import this package and run it from this directory with  
`python -m covidrover`

The file `run.py` calls [covidrover/update_plots.py](covidrover/update_plots.py) and produces a series of plots using available UK government COVID-19 statistics. 

- PNG plots are produced with [matplotlib](https://matplotlib.org/) and written to [output/png](output/png)
- Interactive plots are produced with [Bokeh](https://docs.bokeh.org/en/latest/index.html) as `.html` files in [output/html](output/html)

## Sample output:
![]()![]()

<img src="output/examples/Covid-19MortalityPer100000PeopleByDeprivationDecileBetweenMarchAndMay2020.png?raw=true" alt="drawing" height="200"/><img src="output/examples/FrequencyOfCaseNumbersAsAFunctionOfImd.png?raw=true" alt="drawing" height="200"/>

<img src="output/examples/Cases_2020-06-21_map.png?raw=true" alt="drawing" height="300"/><img src="output/examples/NormalisedIMD_Cases_2020-06-21.png?raw=true" alt="drawing" height="300"/>





