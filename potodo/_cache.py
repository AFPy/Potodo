import pickle
import json
from typing import Optional
from datetime import datetime
import os


def _get_cache_file_content(path: str = ".potodo/cache.json") -> Optional[str]:
    try:
        with open(path, "rb") as handle:
            data = pickle.load(handle)
    except FileNotFoundError:
        return None
    else:
        # data["dt"] = datetime.strptime(data["dt"], "%Y-%m-%d %H:%M:%S.%f")
        return data


def _set_cache_content(obj, path: str = ".potodo/cache.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        pickle.dump(obj, handle)
