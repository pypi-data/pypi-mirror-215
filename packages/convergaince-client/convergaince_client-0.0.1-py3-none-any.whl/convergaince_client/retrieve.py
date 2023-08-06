from __future__ import print_function
import os
from functools import lru_cache
from .lib import get_data
import pandas as pd


@lru_cache(maxsize=None)
def get_dataframe(access_token, api_host, entity):
    url = os.path.join(api_host, "app", entity)
    headers = {"authorization": "Bearer " + access_token}
    resp = get_data(url, headers)
    if resp.status_code == 200:
        props = [
            e["name"]
            for e in resp.json()["meta"]["schema"]
            if not e["name"].startswith("_")
        ]
        df = pd.DataFrame(resp.json()["data"])
        print(props)
        return df[props]
