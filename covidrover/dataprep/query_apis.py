# pylint: disable=C0114,W0105,R1720
"""Module to query UK gov COVID API and paginate the results.
Largely based on the documentation available
at: https://coronavirus.data.gov.uk/developers-guide
"""
from typing import Iterable, Dict, Union, List
from json import dumps
from http import HTTPStatus
from requests import get


StructureType = Dict[str, Union[dict, str]]
FiltersType = Iterable[str]
APIResponseType = Union[List[StructureType], str]


def get_paginated_dataset(
    endpoint: str, filters: FiltersType, structure: StructureType
) -> APIResponseType:
    """
    Extracts paginated data by requesting all of the pages
    and combining the results.

    Parameters
    ----------
    filters: Iterable[str]
        API filters. See the API documentations for additional
        information.

    structure: Dict[str, Union[dict, str]]
        Structure parameter. See the API documentations for
        additional information.

    Returns
    -------
    Union[List[StructureType], str]
        Comprehensive list of dictionaries containing all the data for
        the given ``filters`` and ``structure``.
    """

    api_params = {
        "filters": str.join(";", filters),
        "structure": dumps(structure, separators=(",", ":")),
        "format": "json",
    }

    data = list()

    page_number = 1

    while True:
        # Adding page number to query params
        api_params["page"] = page_number

        response = get(endpoint, params=api_params, timeout=1000)

        if response.status_code >= HTTPStatus.BAD_REQUEST:
            raise RuntimeError(f"Request failed: {response.text}")
        elif response.status_code == HTTPStatus.NO_CONTENT:
            break

        current_data = response.json()
        page_data: List[StructureType] = current_data["data"]

        data.extend(page_data)

        # The "next" attribute in "pagination" will be `None`
        # when we reach the end.
        if current_data["pagination"]["next"] is None:
            break

        page_number += 1

    return data


def run_api_query(
    endpoint_url: str, query_filters: List, query_structure: Dict
) -> List:
    """Set parameters for the API query"""
    json_data = get_paginated_dataset(endpoint_url, query_filters, query_structure)
    return json_data
