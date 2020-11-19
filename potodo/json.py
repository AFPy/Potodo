from datetime import date
from typing import Optional


def json_dateconv(o: object) -> Optional[str]:
    """
    Convert an object to json.

    Args:
        o: (str): write your description
    """
    if isinstance(o, date):
        return o.__str__()
    return None
