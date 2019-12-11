#!/usr/bin/env python3

import sys
import argparse
import statistics

from typing import Tuple, Mapping
from pathlib import Path

try:
    import polib
    import requests
except ImportError:
    print("You need to install polib and requests to be able to run potodo.")
    sys.exit(1)

from potodo._github import get_reservation_list
from potodo._po_file import PoFileStats, get_po_files_from_repo

# TODO: Sort the functions (maybe in different files ?


def initialize_arguments(
    above: int, below: int, offline: bool, hide_reserved: bool
) -> Tuple[int, int, Mapping[str, str]]:
    """Will initialize the arguments as necessary
    """
    if not above:
        # If above isn't specified, then print all files above 0% (all of them)
        above = 0
    if not below:
        # If below isn't specified, then print all files below 100% (all of them)
        below = 100

    if above and below:
        if below < above:
            # If above and below are specified and that below is superior to above, raise an error
            raise ValueError("Below must be inferior to above")

    if not offline and not hide_reserved:
        # If the reservations are to be displayed, then get them
        issue_reservations = get_reservation_list()
    else:
        # Otherwise, an empty list will do the trick
        issue_reservations = {}
    return above, below, issue_reservations


def print_dir_stats(
    directory_name: str, buffer: list, folder_stats: list, printed_list: list
):
    """This function prints the directory name, its stats and the buffer
    """
    if True in printed_list:
        # If at least one of the files isn't done then print the folder stats and file(s)
        # Each time a file is went over True or False is placed in the printed_list list.
        # If False is placed it means it doesnt need to be printed
        print(f"\n\n# {directory_name} ({statistics.mean(folder_stats):.2f}% done)\n")
        print("\n".join(buffer))


def buffer_add(
    buffer: list,
    folder_stats: list,
    printed_list: list,
    po_file_stats: PoFileStats,
    issue_reservations: Mapping[str, str],
    above: int,
    below: int,
    counts: bool
) -> None:
    """Will add to the buffer the information to print about the file is the file isn't translated
    entirely or above or below requested values
    """
    if po_file_stats.percent_translated == 100:
        # If the file is completely translated

        # Add the percentage of the file to the stats of the folder
        folder_stats.append(po_file_stats.percent_translated)
        # Indicate not to print that file
        printed_list.append(False)
        # End the function call without adding anything to the buffer
        return

    if po_file_stats.percent_translated < above:
        # If the file's percent translated is below what is requested

        # Add the percentage of the file to the stats of the folder
        folder_stats.append(po_file_stats.percent_translated)
        # Indicate not to print that file
        printed_list.append(False)
        # End the function call without adding anything to the buffer
        return

    if po_file_stats.percent_translated > below:
        # If the file's percent translated is above what is requested

        # Add the percentage of the file to the stats of the folder
        folder_stats.append(po_file_stats.percent_translated)
        # Indicate not to print that file
        printed_list.append(False)
        # End the function call without adding anything to the buffer
        return

    if not counts:
        buffer.append(
            # The filename
            f"- {po_file_stats.filename:<30} "
            # The number of entries translated / the file size
            + f"{po_file_stats.translated_nb:3d} / {po_file_stats.po_file_size:3d} "
            # The percent of the file translated
            + f"({po_file_stats.percent_translated:5.1f}% translated)"
            # The fuzzies in the file IF fuzzies exists in the file
            + (f", {po_file_stats.fuzzy_nb} fuzzy" if po_file_stats.fuzzy_entries else "")
            # The `reserved by` if the file is reserved unless if the offline/hide_reservation are enabled
            + (
                f", réservé par {issue_reservations[po_file_stats.filename_dir.lower()]}"
                if po_file_stats.filename_dir.lower() in issue_reservations
                else ""
            )
        )
    else:
        todonum = len(po_file_stats.fuzzy_entries) + len(po_file_stats.untranslated_entries)
        buffer.append(
            # The filename
            f"- {po_file_stats.filename:<30} "
            + f"{todonum:3d} to do"
            # The fuzzies in the file IF fuzzies exists in the file
            + (f", including {po_file_stats.fuzzy_nb} fuzzies." if po_file_stats.fuzzy_entries else "")
            # The `reserved by` if the file is reserved unless if the offline/hide_reservation are enabled
            + (
                f", réservé par {issue_reservations[po_file_stats.filename_dir.lower()]}"
                if po_file_stats.filename_dir.lower() in issue_reservations
                else ""
            )
        )
    # Add the percent translated to the folder statistics
    folder_stats.append(po_file_stats.percent_translated)
    # Indicate to print the file
    printed_list.append(True)


def exec_potodo(path: str, above: int, below: int, fuzzy: bool, offline: bool, hide_reserved: bool, counts: bool):
    """
    Will run everything based on the given parameters

    :param path: The path to search into
    :param above: The above threshold
    :param below: The below threshold
    :param fuzzy: Should only fuzzies be printed
    :param offline: Will not connect to internet
    :param hide_reserved: Will not show the reserved files
    """

    # Initialize the arguments
    above, below, issue_reservations = initialize_arguments(
        above, below, offline, hide_reserved
    )

    # Get a dict with the directory name and all po files.
    po_files_and_dirs = get_po_files_from_repo(path)

    for directory_name, po_files in sorted(po_files_and_dirs.items()):
        # For each directory and files in this directory
        buffer: list = []
        folder_stats: list = []
        printed_list: list = []

        for po_file in sorted(po_files):
            # For each file in those files from that directory
            if fuzzy:
                # Ignore files without fuzzies
                if len(po_file.fuzzy_entries) > 0:
                    buffer_add(
                        buffer,
                        folder_stats,
                        printed_list,
                        po_file,
                        issue_reservations,
                        above,
                        below,
                        counts
                    )
                else:
                    pass
            else:
                # All files, with and without fuzzies
                buffer_add(
                    buffer,
                    folder_stats,
                    printed_list,
                    po_file,
                    issue_reservations,
                    above,
                    below,
                    counts
                )
        # Once all files have been processed, print the dir and the files
        print_dir_stats(directory_name, buffer, folder_stats, printed_list)


def main():
    parser = argparse.ArgumentParser(
        prog="potodo", description="List and prettify the po files left to translate"
    )

    parser.add_argument(
        "-p", "--path", type=Path, help="Execute Potodo in the given path"
    )

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

    parser.add_argument("-c", "--counts", action="store_true", help="Render list with count of entries to do (translate or review) instead of percent done")

    args = parser.parse_args()
    # If no path is specified, then use the current path
    if not args.path:
        path = "."
    else:
        path = str(args.path)

    exec_potodo(path, args.above, args.below, args.fuzzy, args.offline, args.no_reserved, args.counts)
