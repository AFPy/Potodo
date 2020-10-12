import os
import pickle
from typing import Dict
from typing import Optional
from typing import List
from pathlib import Path

from potodo._po_file import PoFileStats


def _get_cache_file_content(
    path: str = ".potodo/cache.pickle",
) -> Optional[Dict[Path, List[PoFileStats]]]:
    try:
        with open(path, "rb") as handle:
            data = pickle.load(handle)
    except FileNotFoundError:
        return None
    else:
        return data


def _set_cache_content(
    obj: Dict[Path, List[PoFileStats]], path: str = ".potodo/cache.pickle"
) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "wb") as handle:
        pickle.dump(obj, handle)
