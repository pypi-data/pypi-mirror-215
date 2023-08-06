# exchanges.py

import os
import json
from typing import Dict, Iterable, Optional, List, Union
from dataclasses import dataclass
from pathlib import Path

import requests

from represent import BaseModel

from pycoingecko import CoinGeckoAPI

from crypto_info.base import assets, source

__all__ = [
    "raw_exchanges",
    "Exchange",
    "load_exchanges",
    "sort_exchanges",
    "save_exchanges_logos"
]

coin_gecko_api = CoinGeckoAPI()

raw_exchanges = []

@dataclass(repr=False)
class Exchange(BaseModel):
    """A class to represent exchange data."""

    id: str
    name: str
    url: str
    logo: str
    file: str
    trust: int
    rank: int
    country: str
    beginning: int
    description: Optional[str] = None
# end Exchange

def load_exchanges(
        data: Optional[Optional[Iterable[Dict[str, Union[int, str]]]]] = None,
        exchanges: Optional[Iterable[str]] = None,
        reload: Optional[bool] = False,
        save: Optional[bool] = True
) -> Dict[str, Exchange]:
    """
    Loads the exchanges from the api.

    :param data: The raw exchanges data.
    :param exchanges: The names of the exchanges to include.
    :param reload: The value to reload the data.
    :param save: The value to save new data.

    :return: The exchange objects.
    """

    if os.path.exists(f"{source()}/data/exchanges.json") and not raw_exchanges:
        with open(f"{source()}/data/exchanges.json", "r") as file:
            raw_exchanges[:] = json.load(file)
        # end open
    # end if

    if reload or ((not raw_exchanges) and (data is None)):
        raw_exchanges[:] = coin_gecko_api.get_exchanges_list()

        for exchange in raw_exchanges:
            if exchange["description"] is not None:
                exchange["description"] = (
                    exchange["description"].replace("\n", " ").replace("\r", "")
                ).replace("  ", " ") or None
            # end if

            exchange["beginning"] = exchange["year_established"]
            exchange.pop("year_established")
            exchange["rank"] = exchange["trust_score_rank"]
            exchange.pop("trust_score_rank")
            exchange["trust"] = exchange["trust_score"]
            exchange.pop("trust_score")
            exchange["logo"] = exchange["image"]
            exchange.pop("image")
            exchange.pop("has_trading_incentive")
            exchange.pop("trade_volume_24h_btc")
            exchange.pop("trade_volume_24h_btc_normalized")
            exchange["file"] = (
                str(Path(f"{assets()}/logos/exchanges/{exchange['id']}.jpg"))
            )

        if save:
            with open(f"{source()}/data/exchanges.json", "w") as file:
                json.dump(raw_exchanges, file, indent=4)
            # end open
        # end if
    # end if

    if data is None:
        data = raw_exchanges
    # end if

    if exchanges is not None:
        data = [exchange for exchange in data if exchange["id"] in exchanges]
    # end if

    return {
        exchange["id"]: Exchange(**exchange) for exchange in data
    }
# end load_exchanges

def sort_exchanges(exchanges: Iterable[Exchange]) -> List[Exchange]:
    """
    Sorts the exchange objects.

    :param exchanges: The exchange objects to sort.

    :return: The sorted list of exchanges.
    """

    return sorted(
        exchanges,
        key=lambda exchange: exchange.trust - exchange.rank,
        reverse=True
    )
# end sort_exchanges

def save_exchanges_logos(location: Optional[str] = None) -> Dict[str, str]:
    """
    Saves the logos of the exchanges.

    :param location: The saving location.

    :return: The paths to the logos of the exchanges.
    """

    load_exchanges(data=raw_exchanges or None)

    if location is None:
        location = f"{assets()}/logos/exchanges"
    # end if

    os.makedirs(location, exist_ok=True)

    paths: Dict[str, str] = {}

    for exchange in raw_exchanges:
        path = f"{location}/{exchange['id']}.jpg"

        if os.path.exists(path):
            continue
        # end if

        with open(path, "wb") as file:
            file.write(requests.get(exchange["image"]).content)
        # end open

        paths[exchange['id']] = path
    # end for

    return paths
# end save_exchanges_logos