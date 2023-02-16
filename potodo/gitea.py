import logging
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import requests


class NoRemoteError(Exception):
    """Raise when no remote can be found."""


def get_repo_url(repo_path: Path) -> str:
    """Tries to get the repository url from git commands"""
    try:
        url = subprocess.check_output(
            "git remote get-url --all upstream".split(),
            universal_newlines=True,
            cwd=str(repo_path),
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError:
        try:
            url = subprocess.check_output(
                "git remote get-url --all origin".split(),
                universal_newlines=True,
                cwd=str(repo_path),
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError:
            logging.debug("Cannot find remote 'origin': won't fetch gitea issues.")
            raise NoRemoteError
    logging.debug("Found repo url %s from %s", url, repo_path)
    return url


def get_repo_name(repo_path: Path) -> str:
    """Will get the repository url from git commands then remove useless
    stuff to get ORG/NAME.
    """
    repo_url = get_repo_url(repo_path)
    # Removes useless stuff. If it isn't there then nothing happens

    repo_name = repo_url.replace("https://git.afpy.org/", "")
    repo_name = repo_name.replace("git@git.afpy.org:", "")
    repo_name = repo_name.replace(".git", "")
    repo_name = repo_name.strip("\n")

    logging.debug("Found repo name %s from %s", repo_name, repo_path)
    return repo_name


def _get_reservation_list(repo_path: Path) -> Dict[str, Tuple[Any, Any]]:
    """Will get the repository name then request all the issues and put them in a dict"""  # noqa

    issues: List[Dict[Any, Any]] = []
    repo_url = get_repo_url(repo_path)
    if "git.afpy.org" not in repo_url:
        logging.debug(
            "Remote 'origin' does not point to git.afpy.org: "
            "not fetching issues."
        )
        raise NoRemoteError
    repo_name = get_repo_name(repo_path)
    if repo_name is None:
        return None
    api_url = f"https://git.afpy.org/api/v1/repos/{repo_name}/issues?state=open&type=issues"
    logging.debug("Getting %s", api_url)
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
    offline: bool, hide_reserved: bool, repo_path: Path
) -> Dict[str, Tuple[Any, Any]]:
    """Retrieve info about reservation if needed."""

    if not offline and not hide_reserved:
        logging.info("Getting issue reservations from git.afpy.org")
        # If the reservations are to be displayed, then get them
        try:
            issue_reservations = _get_reservation_list(repo_path)
        except NoRemoteError:
            return {}
    else:
        logging.debug(
            "Reservation list set to be empty because Potodo was started offline"
            " or hiding the reservations."
        )
        # Otherwise, an empty dict will do the trick
        issue_reservations = {}
    return issue_reservations
