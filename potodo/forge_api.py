import logging
import re
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import requests


def _get_reservation_list(api_url: str) -> Dict[str, Tuple[Any, Any]]:
    """Will get the repository name then request all the issues and put them in a dict"""  # noqa
    issues: List[Dict[Any, Any]] = []
    logging.debug("Getting %s", api_url)
    next_url = api_url
    while next_url:
        logging.debug("Getting %s", next_url)
        resp = requests.get(next_url)
        if resp.status_code == 403:
            # Rate limit exceeded
            return {}
        issues.extend(resp.json())
        next_url = resp.links.get("next", {}).get("url")

    resp = requests.get(api_url)
    if resp.status_code == 403:
        # Rate limit exceeded
        return {}
    issues.extend(resp.json())
    logging.debug("Found %s issues", len(issues))

    reservations = {}

    for issue in issues:
        # Maybe find a better way for not using python 3.8 ?
        yes = re.search(r"\w*/[\w\-\.]*\.po", issue["title"])
        if yes:
            creation_date = datetime.strptime(
                issue["created_at"].split("T")[0], "%Y-%m-%d"
            ).date()
            reservations[yes.group()] = (issue["user"]["login"], creation_date)

    logging.debug("Found %s reservations", len(reservations))
    return reservations


def get_issue_reservations(
    offline: bool, hide_reserved: bool, api_url: str,
) -> Dict[str, Tuple[Any, Any]]:
    """Retrieve info about reservation if needed."""

    if not offline and not hide_reserved:
        logging.info("Getting issue reservations from git.afpy.org")
        # If the reservations are to be displayed, then get them
        issue_reservations = _get_reservation_list(api_url)
    else:
        logging.debug(
            "Reservation list set to be empty because Potodo was started offline"
            " or hiding the reservations."
        )
        # Otherwise, an empty dict will do the trick
        issue_reservations = {}
    return issue_reservations
