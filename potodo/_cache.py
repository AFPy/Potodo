import os
import pickle
from datetime import datetime
from datetime import timedelta
from typing import Optional
from typing import Mapping
from typing import Sequence
from potodo._po_file import PoFileStats


def _get_cache_file_content(
    path: str = ".potodo/cache.pickle",
) -> Optional[Mapping[str, Sequence[PoFileStats]]]:
    try:
        with open(path, "rb") as handle:
            data = pickle.load(handle)
    except FileNotFoundError:
        return None
    else:
        content: Optional[Mapping[str, Sequence[PoFileStats]]] = data["data"]
        dt_expiry = data["dt_expiry"]
        if content:
            if dt_expiry < datetime.utcnow():
                return None
            else:
                return content
        else:
            return None


def _set_cache_content(
    obj: Mapping[str, Sequence[PoFileStats]], path: str = ".potodo/cache.pickle"
) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

    to_dump = {"dt_expiry": datetime.utcnow() + timedelta(weeks=1), "data": obj}

    with open(path, "wb") as handle:
        pickle.dump(to_dump, handle)
