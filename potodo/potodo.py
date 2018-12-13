#!/usr/bin/env python3

import sys
import argparse
import statistics

from pathlib import Path

try:
    import polib
    import requests
except ImportError:
    print("You need to install polib and requests to be able to run potodo.")
    sys.exit(1)


def get_gh_issue_reservation(repo: str):
    """
    TODO: Try except if repo unvalid

    Will query given repo and get all issues and return a list of reservations

    :param repo: The repository to query on the API

    :return: Returns a dict containing all issues with `title:login`
    """

    issues = requests.get("https://api.github.com/repos/" + repo + "/issues").json()
    reservations = {
        issue["title"].split()[-1].lower(): issue["user"]["login"] for issue in issues
    }
    return reservations


def get_po_files_from_path(path: str):
    """
    TODO: Try except if path unvalid

    Will get all po files from given path

    :param path: The path to search `po` files for

    :return: Returns a dict will the folder and the po files in it
    """

    po_files = [file for file in Path(path).glob("**/*.po") if ".git/" not in str(file)]

    po_files_per_directory = {
        path.parent.name: set(path.parent.glob("*.po")) for path in po_files
    }
    return po_files_per_directory


def exec_potodo(path: str, above: int, below: int, repo: str):
    """
    Will run everything based on the given parameters

    :param path: The path to search into
    :param above: The above threshold
    :param below: The below threshold
    :param repo: The repository to query for issues
    """

    if not above and below:
        is_all = False
        is_above = False
        is_below = True
    elif not below and above:
        is_all = False
        is_above = True
        is_below = False
    elif not below and not above:
        is_all = True
        is_above = False
        is_below = False
    else:
        raise ValueError(
            "Unexpected error occuped when processing values for above and below."
        )

    if repo:
        issue_reservations = get_gh_issue_reservation(repo)
    else:
        issue_reservations = None

    po_files_per_directory = get_po_files_from_path(path)

    for directory, po_files in sorted(po_files_per_directory.items()):
        buffer = []
        folder_stats = []
        printed_list = []
        for po_file in sorted(po_files):
            po_file_stats = polib.pofile(po_file)
            po_file_stat_percent = po_file_stats.percent_translated()
            if po_file_stat_percent == 100:
                folder_stats.append(po_file_stat_percent)
                printed_list.append(False)
                continue
            if not is_all:
                if is_above:
                    if int(po_file_stat_percent) < above:
                        folder_stats.append(po_file_stat_percent)
                        printed_list.append(False)
                        continue
                elif is_below:
                    if int(po_file_stat_percent) > below:
                        folder_stats.append(po_file_stat_percent)
                        printed_list.append(False)
                        continue
                else:
                    raise ValueError(
                        "Unexpected error: is_above/is_below values shouldn't be like this"
                    )

            t = str(po_file).split("/")[-2:]
            po_file_name = t[0] + "/" + t[1]

            buffer.append(
                f"- {po_file.name:<30} "
                + f"{len(po_file_stats.translated_entries()):3d} / {len(po_file_stats):3d} "
                + f"({po_file_stat_percent:5.1f}% translated)"
                + (
                    f", {len(po_file_stats.fuzzy_entries())} fuzzy"
                    if po_file_stats.fuzzy_entries()
                    else ""
                )
                + (
                    f", réservé par {issue_reservations[po_file_name.lower()]}"
                    if po_file_name.lower() in issue_reservations
                    else ""
                )
            )
            folder_stats.append(po_file_stat_percent)
            printed_list.append(True)
        if True in printed_list:
            print(f"\n\n# {directory} ({statistics.mean(folder_stats):.2f}% done)\n")
            print("\n".join(buffer))


def main():
    """
    TODO: Add variable to skip github issues
    TODO: Remove requirement of -r and fetch the repo name manually
    TODO: Add json output possibility
    TODO: -l for path line by line --matching-files
    TODO: classify ?
    TODO: Make it so you can specify both: list todos above 50 but below 60 (between 50 and 60)
    """

    parser = argparse.ArgumentParser(
        prog="potodo", description="List and prettify the po files left to translate"
    )

    parser.add_argument(
        'path',
        type=Path,
        help="Execute Potodo in the given path",
    )

    parser.add_argument(
        'repo',
        type=str,
        help="Repo in the form of ORG/REPO to display if translation is reserved in issues",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-a",
        "--above",
        type=int,
        help="Will list all TODOs ABOVE given INT%% completion",
    )
    group.add_argument(
        "-b",
        "--below",
        type=int,
        help="Will list all TODOs BELOW given INT%% completion",
    )

    args = parser.parse_args()
    if not args.path:
        path = "."
    else:
        path = str(args.path)

    exec_potodo(path, args.above, args.below, args.repo)
