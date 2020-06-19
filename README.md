# COVID-19 data analysis tool

[![Build Status](https://travis-ci.org/harryjmoss/COVIDRover.svg?branch=master)](https://travis-ci.org/harryjmoss/COVIDRover)

Tool to query the latest available statistics on COVID-19 cases in the UK and perform analysis.

### Data sources
- COVID deaths and cases data is taken from https://coronavirus.data.gov.uk/
- Contains public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
- Deprivation index data is taken from the UK Ministry of Housing, Communities & Local Government and is available via [https://opendatacommunities.org/](https://opendatacommunities.org/resource?uri=http%3A%2F%2Fopendatacommunities.org%2Fdata%2Fsocietal-wellbeing%2Fimd2019%2Findices) under the Open Government Licence v3.0

'Deprivation' is derived from the 'Index of multiple deprivation' (IMD) and is comprised of multiple factors. IMD in England is defined within [this document](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/853811/IoD2019_FAQ_v4.pdf). The definition used in this analysis is a population-weighted average of the combined scores of the smaller areas that comprise each region considered. 'IMD' in this context refers to this averaged score.
