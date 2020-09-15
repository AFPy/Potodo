import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import requests


def get_repo_url(repo_path: Path) -> str:
    """Tries to get the repository url from git commands
    """
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
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f'Unknown error. `{" ".join(e.cmd)}` returned "{e.output.rstrip()}".'
            )
    return url


def get_repo_name(repo_path: Path) -> str:
    """Will get the repository url from git commands then remove useless
    stuff to get ORG/NAME.
    """
    repo_url = get_repo_url(repo_path)
    # Removes useless stuff. If it isn't there then nothing happens

    repo_name = repo_url.replace("https://github.com/", "")
    repo_name = repo_name.replace("git@github.com:", "")
    repo_name = repo_name.replace(".git", "")
    repo_name = repo_name.strip("\n")

    return repo_name


def get_reservation_list(repo_path: Path) -> Dict[str, Tuple[Any, Any]]:
    """Will get the repository name then request all the issues and put them in a dict
    """

    issues: List[Dict[Any, Any]] = []
    next_url = (
        "https://api.github.com/repos/"
        + get_repo_name(repo_path)
        + "/issues?state=open"
    )
    while next_url:
        resp = requests.get(next_url)
        issues.extend(resp.json())
        next_url = resp.links.get("next", {}).get("url")

    reservations = {}

    for issue in issues:
        # Maybe find a better way for not using python 3.8 ?
        yes = re.search(r"\w*/\w*\.po", issue["title"])
        if yes:
            datetime_object = datetime.strptime(
                issue["created_at"].split("T")[0], "%Y-%m-%d"
            ).date()
            reservations[yes.group()] = (issue["user"]["login"], datetime_object)

    return reservations
