import logging
import os
from pathlib import Path
from typing import Any
from typing import List
from typing import Mapping


def check_args(
    path: str,
    exclude: List[str],
    below: int,
    above: int,
    verbose: int,
    only_fuzzy: bool,
    offline: bool,
    hide_reserved: bool,
    counts: bool,
    json_format: bool,
    exclude_fuzzy: bool,
    exclude_reserved: bool,
    only_reserved: bool,
    show_reservation_dates: bool,
    no_cache: bool,
    is_interactive: bool,
    **kwargs: Any,
) -> Mapping[str, Any]:
    # If below is lower than above, raise an error
    if below < above:
        print("Potodo: 'below' value must be greater than 'above' value.")
        exit(1)

    if json_format and is_interactive:
        print(
            "Potodo: Json format and interactive modes cannot be activated at the same time."
        )
        exit(1)

    if is_interactive:
        try:
            import termios  # noqa
        except ImportError:
            import platform

            print(
                'Potodo: "{}" is not supported for interactive mode'.format(
                    platform.system()
                )
            )

    if exclude_fuzzy and only_fuzzy:
        print("Potodo: Cannot pass --exclude-fuzzy and --only-fuzzy at the same time.")
        exit(1)

    if exclude_reserved and only_reserved:
        print(
            "Potodo: Cannot pass --exclude-reserved and --only-reserved at the same time."
        )
        exit(1)

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
        "exclude": exclude,
        "logging_level": logging_level,
    }
