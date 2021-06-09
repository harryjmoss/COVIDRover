# pylint: disable=C0114,W0105,R1720
"""Module to query UK gov COVID API and paginate the results.
Largely based on the documentation available
at: https://coronavirus.data.gov.uk/developers-guide
"""
from typing import Iterable, Dict, Union, List
from json import dumps
from http import HTTPStatus
from requests import get
from uk_covid19 import Cov19API

StructureType = Dict[str, Union[dict, str]]
FiltersType = Iterable[str]
APIResponseType = Union[List[StructureType], str]

def run_api_query(
    query_filters: List, query_structure: Dict
) -> List:
    """Set parameters for the API query"""
    api = Cov19API(filters=query_filters, structure=query_structure)
    dataframe = api.get_dataframe()
    #json_data = get_paginated_dataset(endpoint_url, query_filters, query_structure)
    return dataframe
