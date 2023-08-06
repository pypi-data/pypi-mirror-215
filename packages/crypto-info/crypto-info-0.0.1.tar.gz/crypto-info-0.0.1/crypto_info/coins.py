# coins.py

import json
import os
from typing import Optional, Iterable, Dict, Any, Union
from dataclasses import dataclass

from represent import BaseModel

import pandas as pd

from crypto_info.base import source

__all__ = [
    "raw_coins",
    "Coin",
    "load_coins",
    "table_to_json",
    "table_from_json"
]

raw_coins = []

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

@dataclass(repr=False)
class Coin(BaseModel):
    """A class to represent the data of a coin."""

    id: str
    name: str
    price_usd: float
# end Coin

def load_coins(
        data: Optional[Optional[Iterable[Dict[str, Union[int, str]]]]] = None,
        coins: Optional[Iterable[str]] = None,
        reload: Optional[bool] = False,
        save: Optional[bool] = True
) -> Dict[str, Coin]:
    """
    Loads the data of the coins.

    :param data: The raw exchanges data.
    :param coins: The names of the assets.
    :param reload: The value to reload the data.
    :param save: The value to save new data.

    :return: The coins' data.
    """

    if os.path.exists(f"{source()}/data/coins.json") and not raw_coins:
        with open(f"{source()}/data/coins.json", "r") as file:
            raw_coins[:] = json.load(file)
        # end open
    # end if

    if reload or ((not raw_coins) and (data is None)):
        df = pd.read_html("https://coinmarketcap.com/")[0]
        df = df[list(df.columns)[2:4]]

        names = []
        titles = []

        for i, text in enumerate(df["Name"], start=1):
            if str(i) in text:
                title = text[:text.find(str(i))]
                name = text[text.find(str(i)) + len(str(i)):]

            else:
                j = 0

                for j in range(len(text)):
                    if text[j:] == text[j:].upper():
                        break
                    # end if
                # end for

                title = text[:j]
                name = text[j:]
            # end if

            if not name:
                continue
            # end if

            if not title:
                title = name
            # end if

            titles.append(title)
            names.append(name)
        # end for

        df = pd.DataFrame(
            {
                "id": names,
                "name": titles,
                "price_usd": [
                    float(value[1:].replace(",", ""))
                    for value in df["Price"]
                ]
            },
            index=df.index
        )

        raw_coins[:] = list(table_to_json(df).values())

        if save:
            with open(f"{source()}/data/coins.json", "w") as file:
                json.dump(raw_coins, file, indent=4)
            # end open
        # end if

        data = raw_coins
    # end if

    if data is None:
        data = raw_coins
    # end if

    if coins is not None:
        data = [coin for coin in data if coin["id"] in coins]
    # end if

    return {
        coin["name"]: Coin(
            id=coin["id"],
            name=coin["name"],
            price_usd=coin["price_usd"]
        ) for coin in data
    }
# end load_coins