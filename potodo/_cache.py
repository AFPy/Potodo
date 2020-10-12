import os
import pickle
from datetime import datetime
from datetime import timedelta
from typing import Optional
from typing import Tuple


def _get_cache_file_content(
    path: str = ".potodo/cache.pickle",
) -> Tuple[Optional[datetime], Optional[dict]]:
    try:
        with open(path, "rb") as handle:
            data = pickle.load(handle)
    except FileNotFoundError:
        return None, None
    else:
        return data["dt_expiry"], data["data"]


def _set_cache_content(obj, path: str = ".potodo/cache.pickle"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    to_dump = {"dt_expiry": datetime.utcnow() + timedelta(weeks=1), "data": obj}

    with open(path, "wb") as handle:
        pickle.dump(to_dump, handle)
