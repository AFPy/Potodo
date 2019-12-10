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

from potodo._github import get_reservation_list
from potodo._po_file import PoFile


# def initialize_arguments(above: int, below: int, matching_files: bool, offline: bool, hide_reserved: bool):
def initialize_arguments(above: int, below: int, offline: bool, hide_reserved: bool):
    if not above:
        above = 0
    if not below:
        below = 100

    if above and below:
        if below < above:
            raise ValueError("Below must be inferior to above")

    # if not matching_files and not offline and not hide_reserved:
    #     issue_reservations = get_reservation_list()
    # else:
    #     issue_reservations = []
    if not offline and not hide_reserved:
        issue_reservations = get_reservation_list()
    else:
        issue_reservations = []
    return above, below, issue_reservations


def print_dir_stats(directory_name: str, buffer: list, folder_stats: list, printed_list: list, fuzzy: bool):
    if True in printed_list:
        print(f"\n\n# {directory_name} ({statistics.mean(folder_stats):.2f}% done)\n")
        print("\n".join(buffer))


# def print_matching_files(directory_name: str, po_files: list, fuzzy: bool):
#     for po_file in po_files:
#         po_file_stats = po_file.pofile
#         if fuzzy:
#             if len(po_file_stats.fuzzy_entries()) > 0:
#                 print(directory_name + "/" + po_file.filename)
#             else:
#                 continue
#         else:
#             print(directory_name + "/" + po_file.filename)


def buffer_add(buffer: list, folder_stats: list, printed_list: list, po_file: PoFile, issue_reservations: dict, directory_name: str, above: int, below: int):

    if po_file.percent_translated == 100:
        # Add the percentage of the file to the stats of the folder
        folder_stats.append(po_file.percent_translated)
        # Indicate not to print that file
        printed_list.append(False)
        return buffer, folder_stats, printed_list

    if po_file.percent_translated < above:
        # Add the percentage of the file to the stats of the folder
        folder_stats.append(po_file.percent_translated)
        # Indicate not to print that file
        printed_list.append(False)
        return buffer, folder_stats, printed_list

    if po_file.percent_translated > below:
        # Add the percentage of the file to the stats of the folder
        folder_stats.append(po_file.percent_translated)
        # Indicate not to print that file
        printed_list.append(False)
        return buffer, folder_stats, printed_list

    buffer.append(
        f"- {po_file.filename:<30} "
        + f"{po_file.translated_nb:3d} / {po_file.po_file_size:3d} "
        + f"({po_file.percent_translated:5.1f}% translated)"
        + (
            f", {po_file.fuzzy_nb} fuzzy"
            if po_file.fuzzy_entries
            else ""
        )
        + (
            f", réservé par {issue_reservations[po_file.get_dir_and_filename(directory_name).lower()]}"
            if po_file.get_dir_and_filename(directory_name).lower() in issue_reservations
            else ""
        )
    )
    folder_stats.append(po_file.percent_translated)
    printed_list.append(True)

    return buffer, folder_stats, printed_list


def exec_potodo(
    path: str,
    above: int,
    below: int,
    # matching_files: bool,
    fuzzy: bool,
    offline: bool,
    hide_reserved: bool,
):
    """
    Will run everything based on the given parameters

    :param path: The path to search into
    :param above: The above threshold
    :param below: The below threshold
    # :param matching_files: Should the file paths be printed instead of normal output
    :param fuzzy: Should only fuzzies be printed
    :param offline: Will not connect to internet
    :param hide_reserved: Will not show the reserved files
    """

    # above, below, issue_reservations = initialize_arguments(above, below, matching_files, offline, hide_reserved)
    above, below, issue_reservations = initialize_arguments(above, below, offline, hide_reserved)

    from potodo._po_file import get_po_files_from_repo

    po_files_and_dirs = get_po_files_from_repo(path)

    for directory_name, po_files in sorted(po_files_and_dirs.items()):
        # if matching_files:
        #     print_matching_files(directory_name, po_files, fuzzy)
        buffer = []
        folder_stats = []
        printed_list = []

        for po_file in sorted(po_files):
            if fuzzy:
                # ignore files without fuzzies
                if len(po_file.fuzzy_entries) > 0:
                    buffer, folder_stats, printed_list = buffer_add(buffer, folder_stats, printed_list, po_file, issue_reservations, directory_name, above, below)
                else:
                    pass
            else:
                # all files, with and without fuzzies
                buffer, folder_stats, printed_list = buffer_add(buffer, folder_stats, printed_list, po_file, issue_reservations, directory_name, above, below)
        # Once all files have been processed, print the dir and the files
        print_dir_stats(directory_name, buffer, folder_stats, printed_list, fuzzy)


def main():
    parser = argparse.ArgumentParser(
        prog="potodo", description="List and prettify the po files left to translate"
    )

    parser.add_argument(
        "-p", "--path", type=Path, help="Execute Potodo in the given path"
    )

    # Removed as it needs to be refactored

    # parser.add_argument(
    #     "-l",
    #     "--matching-files",
    #     action="store_true",
    #     help="Suppress normal output; instead print the name of each matching po file from which output would normally "
    #     "have been printed.",
    # )

    parser.add_argument(
        "-f",
        "--fuzzy",
        action="store_true",
        help="Will only print files marked as fuzzys",
    )

    parser.add_argument(
        "-o",
        "--offline",
        action="store_true",
        help="Will not do any fetch to GitHub/online if given",
    )

    parser.add_argument(
        "-n",
        "--no-reserved",
        action="store_true",
        help="Will not print the info about reserved files",
    )

    parser.add_argument(
        "-a",
        "--above",
        type=int,
        help="Will list all TODOs ABOVE given INT%% completion",
    )
    parser.add_argument(
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

    exec_potodo(
        path,
        args.above,
        args.below,
        # args.matching_files,
        args.fuzzy,
        args.offline,
        args.no_reserved,
    )
