# coins.py

import json
import os
from typing import Optional, Iterable, Dict, Union
from dataclasses import dataclass

from represent import BaseModel

import pandas as pd

from crypto_info.base import source
from crypto_info.table import table_to_json

__all__ = [
    "raw_coins",
    "Coin",
    "load_coins",
    "load_coins_data",
    "extract_coins_data"
]

raw_coins = []

@dataclass(repr=False)
class Coin(BaseModel):
    """A class to represent the data of a coin."""

    id: str
    name: str
    price_usd: float
# end Coin

CoinsDats = Dict[str, Dict[str, Union[str, float]]]

def load_coins_data(
        coins: Optional[Iterable[str]] = None,
        reload: Optional[bool] = False,
        save: Optional[bool] = True
) -> CoinsDats:
    """
    Loads the data of the coins.

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

    if reload or (not raw_coins):
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
    # end if

    data = raw_coins

    if coins is not None:
        data = [coin for coin in data if coin["id"] in coins]
    # end if

    return {coin["id"]: coin for coin in data}
# end load_coins_data

def load_coins(
        data: Optional[CoinsDats] = None,
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

    if data is None:
        data = load_coins_data(coins=coins, reload=reload, save=save)
    # end if

    return {key: Coin(**coin) for key, coin in data.items()}
# end load_coins

def extract_coins_data(coins: Union[Iterable[Coin], Dict[str, Coin]]) -> CoinsDats:
    """
    Extracts the data from the coins.

    :param coins: The coins to extract.

    :return: The extracted data of the coins.
    """

    if not isinstance(coins, dict):
        coins = {coin.id: coin for coin in coins}
    # end if

    return {
        key: coin.__dict__.copy()
        for key, coin in coins.items()
    }
# end extract_coins_data