import requests

from subprocess import getoutput


def get_repo_url():
    url = getoutput("git remote get-url --all upstream")
    if "fatal" in url:
        url = getoutput("git remote get-url --all origin")
    if "fatal" in url:
        raise ValueError(
            f"Unknown error. `git get-url --all upstream|origin` returned {url}"
        )
    return url


def get_repo_name():
    repo_url: str = get_repo_url()
    repo_url = repo_url.replace("https://github.com/", "")
    repo_url = repo_url.replace("git@github.com:", "")
    repo_name = repo_url.replace(".git", "")
    return repo_name


def get_reservation_list():
    issues = requests.get(
        "https://api.github.com/repos/" + get_repo_name() + "/issues"
    ).json()
    reservations = {
        issue["title"].split()[-1].lower(): issue["user"]["login"] for issue in issues
    }
    return reservations
