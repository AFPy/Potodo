import re
import requests

from subprocess import check_output


def get_repo_url() -> str:
    """Tries to get the repository url from git commands
    """
    url: str = check_output(
        "git remote get-url --all upstream", universal_newlines=True
    )
    if "fatal" in url:
        url = check_output("git remote get-url --all origin", universal_newlines=True)
    if "fatal" in url:
        # If the commands didn't work
        raise ValueError(
            f"Unknown error. `git get-url --all upstream|origin` returned {url}"
        )
    return url


def get_repo_name() -> str:
    """Will get the repository url from git commands then remove useless stuff to get ORG/NAME
    """
    repo_url: str = get_repo_url()
    # Removes useless stuff. If it isn't there then nothing happens
    repo_name = re.sub("https://github.com/", "", repo_url)
    repo_name = re.sub("git@github.com:", "", repo_name)
    repo_name = re.sub(".git", "", repo_name)
    return repo_name


def get_reservation_list() -> dict:
    """Will get the repository name then request all the issues and put them in a dict
    """
    # Gets the issues into a dict
    issues = requests.get(
        "https://api.github.com/repos/" + get_repo_name() + "/issues"
    ).json()
    # Creates the issue dict with the name and the login
    reservations: dict = {
        issue["title"].split()[-1].lower(): issue["user"]["login"] for issue in issues
    }
    return reservations
