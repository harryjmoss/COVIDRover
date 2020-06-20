# COVID-19 data analysis tool

[![Build Status](https://travis-ci.org/harryjmoss/COVIDRover.svg?branch=master)](https://travis-ci.org/harryjmoss/COVIDRover)

Tool to query the latest available statistics on COVID-19 cases in the UK and perform analysis.

### Data sources
- COVID deaths and cases data is taken from https://coronavirus.data.gov.uk/ and is licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)
- Deprivation index data is taken from the UK Ministry of Housing, Communities & Local Government and is available via [https://opendatacommunities.org/](https://opendatacommunities.org/resource?uri=http%3A%2F%2Fopendatacommunities.org%2Fdata%2Fsocietal-wellbeing%2Fimd2019%2Findices) under the Open Government Licence v3.0
- [Population data](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationprojections/datasets/localauthoritiesinenglandtable2]https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationprojections/datasets/localauthoritiesinenglandtable2) Source: Office for National Statistics (ONS) licensed under the Open Government Licence v3.0
- [Geographical data](https://hub.arcgis.com/datasets/a8531598f29f44e7ad455abb6bf59c60_0) Source: Office for National Statistics licensed under the Open Government Licence v.3.0

'Deprivation' is derived from the 'Index of multiple deprivation' (IMD) and is comprised of multiple factors. IMD in England is defined within [this document](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/853811/IoD2019_FAQ_v4.pdf). The definition used in this analysis is a population-weighted average of the combined scores of the smaller areas that comprise each region considered. 'IMD' in this context refers to this averaged score.


## Setup
Install dependent packages with:  
`pip install -r requirements.txt`

The first time the program runs, geographical data is collected as a geoJSON file from the ONS Open Geography Portal if it does not exist in the `data` directory. The geoJSON is trimmed down and saved as a geoJSON file in the the `data` directory for future use. As the file is quite large(!), this (should) only happen the first time you run the package.

## Running

