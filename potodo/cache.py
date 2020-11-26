import logging
import os
import pickle
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from typing import cast
from typing import Dict

from potodo import __version__ as VERSION
from potodo.po_file import PoFileStats


def get_cache_file_content(
    cache_args: Any,
    path: str = ".potodo/cache.pickle",
) -> Dict[Path, PoFileStats]:
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
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {"version": VERSION, "args": cache_args, "data": obj}
    with NamedTemporaryFile(
        mode="wb", delete=False, dir=str(Path(path).parent), prefix=Path(path).name
    ) as tmp:
        pickle.dump(data, tmp)
    os.rename(tmp.name, path)
    logging.debug("Set cache to %s", path)
