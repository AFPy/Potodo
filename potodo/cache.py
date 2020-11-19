import logging
import os
import pickle
from pathlib import Path
from typing import cast
from typing import Dict
from typing import Any

from potodo import __version__ as VERSION
from potodo.po_file import PoFileStats


def get_cache_file_content(
    cache_args: Any,
    path: str = ".potodo/cache.pickle",
) -> Dict[Path, PoFileStats]:
    """
    Get cache file content

    Args:
        cache_args: (str): write your description
        path: (str): write your description
    """
    logging.debug("Trying to load cache from %s", path)
    try:
        with open(path, "rb") as handle:
            data = pickle.load(handle)
    except FileNotFoundError:
        logging.warning("No cache found")
        return {}
    else:
        logging.debug("Found cache")
        if data.get("version") != VERSION or cache_args != data.get("args"):
            logging.info("Found old cache, ignored it.")
            return {}
        else:
            return cast(Dict[Path, PoFileStats], data["data"])


def set_cache_content(
    obj: Dict[Path, PoFileStats], cache_args: Any, path: str = ".potodo/cache.pickle"
) -> None:
    """
    Set the cache.

    Args:
        obj: (todo): write your description
        cache_args: (dict): write your description
        path: (str): write your description
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {"version": VERSION, "args": cache_args, "data": obj}
    with open(path, "wb") as handle:
        pickle.dump(data, handle)
    logging.debug("Set cache to %s", path)
