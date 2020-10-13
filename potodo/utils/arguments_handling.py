import logging
import os
from pathlib import Path
from typing import Any
from typing import List
from typing import Mapping


def check_args(
    path: str, exclude: List[str], below: int, above: int, verbose: int, **kwargs: Any
) -> Mapping[str, Any]:
    # If below is lower than above, raise an error
    if below < above:
        raise ValueError("'below' must be greater than 'above'.")

    # If no path is specified, use current directory
    if not path:
        path = os.getcwd()

    logging_level = None
    if verbose:
        if verbose == 1:
            # Will only show ERROR and CRITICAL
            logging_level = logging.WARNING
        if verbose == 2:
            # Will only show ERROR, CRITICAL and WARNING
            logging_level = logging.INFO
        if verbose >= 3:
            # Will show INFO WARNING ERROR DEBUG CRITICAL
            logging_level = logging.DEBUG
    else:
        # Disable all logging
        logging.disable(logging.CRITICAL)

    # Convert strings to `Path` objects and make them absolute
    return {
        "path": Path(path).resolve(),
        "exclude": [Path(path).resolve() for path in exclude],
        "logging_level": logging_level,
    }
