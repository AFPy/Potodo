import itertools
import logging
import os
from datetime import date
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Optional

from potodo._po_file import is_within


def setup_logging(logging_level: int) -> None:
    print(logging_level)
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s %(levelname)-8s [%(filename)s:"
        "%(lineno)d %(funcName)s()] %(message)s",
        datefmt="%d-%m-%Y:%H:%M:%S",
    )
    # Silencing some loggers
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def json_dateconv(o: object) -> Optional[str]:
    if isinstance(o, date):
        return o.__str__()
    return None


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


def get_po_files_per_directory_no_stats(
    repo_path: Path, exclude: Iterable[Path]
) -> Dict[str, List[str]]:
    all_po_files = [
        file
        for file in repo_path.rglob("*.po")
        if not any(is_within(file, excluded) for excluded in exclude)
    ]
    files_per_dir = {
        name: set(files)
        # We assume the output of rglob to be sorted,
        # so each 'name' is unique within groupby
        for name, files in itertools.groupby(
            all_po_files, key=lambda path: path.parent.name
        )
    }
    return {
        directory: [po_file.name for po_file in po_files]
        for directory, po_files in files_per_dir.items()
    }


def get_dir_list(repo_path: Path, exclude: Iterable[Path]) -> List[str]:
    return list(
        set(
            [
                file.parent.name
                for file in repo_path.rglob("*.po")
                if not any(is_within(file, excluded) for excluded in exclude)
            ]
        )
    )


def get_files_from_dir(
    directory: str, repo_path: Path, exclude: Iterable[Path]
) -> List[str]:
    path = Path(str(repo_path) + "/" + directory)
    return [
        file.name
        for file in path.rglob("*.po")
        if not any(is_within(file, excluded) for excluded in exclude)
    ]
