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
    endpoint: str, filters: FiltersType, structure: StructureType, as_csv: bool = False
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

    as_csv: bool
        Return the data as CSV. [default: ``False``]

    Returns
    -------
    Union[List[StructureType], str]
        Comprehensive list of dictionaries containing all the data for
        the given ``filters`` and ``structure``.
    """

    api_params = {
        "filters": str.join(";", filters),
        "structure": dumps(structure, separators=(",", ":")),
        "format": "json" if not as_csv else "csv",
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

        if as_csv:
            csv_content = response.content.decode()

            # Removing CSV header (column names) where page
            # number is greater than 1.
            if page_number > 1:
                data_lines = csv_content.split("\n")[1:]
                csv_content = str.join("\n", data_lines)

            data.append(csv_content.strip())
            page_number += 1
            continue

        current_data = response.json()
        page_data: List[StructureType] = current_data["data"]

        data.extend(page_data)

        # The "next" attribute in "pagination" will be `None`
        # when we reach the end.
        if current_data["pagination"]["next"] is None:
            break

        page_number += 1

    if not as_csv:
        return data

    # Concatenating CSV pages
    return str.join("\n", data)


def run_api_query(endpoint_url):
    """Set parameters for the API query"""
    query_filters = ["areaType=ltla"]

    query_structure = {
        "date": "date",
        "name": "areaName",
        "code": "areaCode",
        "daily": "newCasesBySpecimenDate",
        "cumulative": "cumCasesBySpecimenDate",
        "caseRate": "cumCasesBySpecimenDateRate",
        "newDeaths": "newDeaths28DaysByDeathDate",
        "cDeaths": "cumDeaths28DaysByDeathDate",
        "deathRate": "cumDeaths28DaysByDeathDateRate",
    }

    json_data = get_paginated_dataset(endpoint_url, query_filters, query_structure)
    return json_data
