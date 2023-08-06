# table.py

from typing import Dict, Any
import json

import pandas as pd

__all__ = [
    "table_to_json",
    "table_from_json"
]

def table_to_json(dataset: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Converts the data of the dataset to json.

    :param dataset: The dataset to process.

    :return: The json representation of the data.
    """

    return json.loads(dataset.to_json(orient='index'))
# end table_to_json

def table_from_json(data: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """
    Converts the data from json format into a dataframe object.

    :param data: The json data to process.

    :return: The data frame object.
    """

    return pd.read_json(json.dumps(data), orient="index")
# end table_from_json