#!/usr/bin/env python3

import argparse
import os
import json
import statistics

from typing import Any, Dict, List, Mapping, Sequence, Tuple

from potodo import __version__
from potodo._github import get_reservation_list
from potodo._po_file import PoFileStats, get_po_files_from_repo

# TODO: Sort the functions (maybe in different files ?


def initialize_arguments(
    above: int, below: int, offline: bool, hide_reserved: bool, repo_path: str
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
            # If above and below are specified and that below is superior to above,
            # raise an error
            raise ValueError("Below must be inferior to above")

    if not offline and not hide_reserved:
        # If the reservations are to be displayed, then get them
        issue_reservations = get_reservation_list(repo_path)
    else:
        # Otherwise, an empty list will do the trick
        issue_reservations = {}
    return above, below, issue_reservations


def print_dir_stats(
    directory_name: str,
    buffer: Sequence[str],
    folder_stats: Sequence[int],
    printed_list: Sequence[bool],
) -> None:
    """This function prints the directory name, its stats and the buffer
    """
    if True in printed_list:
        # If at least one of the files isn't done then print the
        # folder stats and file(s) Each time a file is went over True
        # or False is placed in the printed_list list.  If False is
        # placed it means it doesnt need to be printed
        print(f"\n\n# {directory_name} ({statistics.mean(folder_stats):.2f}% done)\n")
        print("\n".join(buffer))


def add_dir_stats(
    directory_name: str,
    buffer: List[Dict[str, str]],
    folder_stats: Sequence[int],
    printed_list: Sequence[bool],
    all_stats: List[Dict[str, Any]],
) -> None:
    """Appends directory name, its stats and the buffer to stats
    """
    if any(printed_list):
        pc_translated = statistics.mean(folder_stats)
        all_stats.append(
            dict(
                name=f"{directory_name}/",
                percent_translated=float(f"{pc_translated:.2f}"),
                files=buffer,
            )
        )


def exec_potodo(
    path: str,
    exclude: List[str],
    above: int,
    below: int,
    fuzzy: bool,
    offline: bool,
    hide_reserved: bool,
    counts: bool,
    json_format: bool,
) -> None:
    """
    Will run everything based on the given parameters

    :param path: The path to search into
    :param exclude: folders or files to be ignored
    :param above: The above threshold
    :param below: The below threshold
    :param fuzzy: Should only fuzzies be printed
    :param offline: Will not connect to internet
    :param hide_reserved: Will not show the reserved files
    :param counts: Render list with counts not percentage
    :param json_format: Format output as JSON.
    """

    # Initialize the arguments
    above, below, issue_reservations = initialize_arguments(
        above, below, offline, hide_reserved, path
    )

    # Get a dict with the directory name and all po files.
    po_files_and_dirs = get_po_files_from_repo(path, exclude)

    dir_stats: List[Any] = []
    for directory_name, po_files in sorted(po_files_and_dirs.items()):
        # For each directory and files in this directory
        buffer: List[Any] = []
        folder_stats: List[int] = []
        printed_list: List[bool] = []

        for po_file in sorted(po_files):
            # For each file in those files from that directory
            if not fuzzy or po_file.fuzzy_entries:
                buffer_add(
                    buffer,
                    folder_stats,
                    printed_list,
                    po_file,
                    issue_reservations,
                    above,
                    below,
                    counts,
                    json_format,
                )

        # Once all files have been processed, print the dir and the files
        # or store them into a dict to print them once all directories have
        # been processed.
        if json_format:
            add_dir_stats(directory_name, buffer, folder_stats, printed_list, dir_stats)
        else:
            print_dir_stats(directory_name, buffer, folder_stats, printed_list)

    if json_format:
        print(json.dumps(dir_stats, indent=4, separators=(",", ": "), sort_keys=False))


def buffer_add(
    buffer: List[Any],
    folder_stats: List[int],
    printed_list: List[bool],
    po_file_stats: PoFileStats,
    issue_reservations: Mapping[str, str],
    above: int,
    below: int,
    counts: bool,
    json_format: bool,
) -> None:
    """Will add to the buffer the information to print about the file is
    the file isn't translated entirely or above or below requested
    values.
    """
    # If the file is completely translated,
    # or is translated below what's requested
    # or is translated above what's requested
    if (
        po_file_stats.percent_translated == 100
        or po_file_stats.percent_translated < above
        or po_file_stats.percent_translated > below
    ):

        # add the percentage of the file to the stats of the folder
        folder_stats.append(po_file_stats.percent_translated)

        if not json_format:
            # don't print that file
            printed_list.append(False)

        # return without adding anything to the buffer
        return

    fuzzy_entries = po_file_stats.fuzzy_entries
    untranslated_entries = po_file_stats.untranslated_entries
    # nb of fuzzies in the file IF there are some fuzzies in the file
    fuzzy_nb = po_file_stats.fuzzy_nb if fuzzy_entries else 0
    # number of entries translated
    translated_nb = po_file_stats.translated_nb
    # file size
    po_file_size = po_file_stats.po_file_size
    # percentage of the file already translated
    percent_translated = po_file_stats.percent_translated
    # `reserved by` if the file is reserved
    # unless the offline/hide_reservation are enabled
    reserved_by = issue_reservations.get(po_file_stats.filename_dir.lower(), None)

    directory = po_file_stats.directory
    filename = po_file_stats.filename
    path = po_file_stats.path

    if json_format:

        # the order of the keys is the display order
        d = dict(
            name=f"{directory}/{filename.replace('.po', '')}",
            path=str(path),
            entries=po_file_size,
            fuzzies=fuzzy_nb,
            translated=translated_nb,
            percent_translated=percent_translated,
            reserved_by=reserved_by,
        )

        buffer.append(d)

    else:
        s = f"- {filename:<30} "  # The filename

        if counts:
            missing = len(fuzzy_entries) + len(untranslated_entries)
            s += f"{missing:3d} to do"
            s += f", including {fuzzy_nb} fuzzies." if fuzzy_nb else ""

        else:
            s += f"{translated_nb:3d} / {po_file_size:3d} "
            s += f"({percent_translated:5.1f}% translated)"
            s += f", {fuzzy_nb} fuzzy" if fuzzy_nb else ""

        if reserved_by is not None:
            s += f", réservé par {reserved_by}"

        buffer.append(s)

    # Add the percent translated to the folder statistics
    folder_stats.append(po_file_stats.percent_translated)
    # Indicate to print the file
    printed_list.append(True)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="potodo", description="List and prettify the po files left to translate.",
    )

    parser.add_argument(
        "-p", "--path", help="execute Potodo in path", metavar="path",
    )

    parser.add_argument(
        "-e",
        "--exclude",
        nargs="+",
        default=[],
        help="exclude from search",
        metavar="path",
    )

    parser.add_argument(
        "-a",
        "--above",
        metavar="X",
        type=int,
        help="list all TODOs above given X%% completion",
    )

    parser.add_argument(
        "-b",
        "--below",
        metavar="X",
        type=int,
        help="list all TODOs below given X%% completion",
    )

    parser.add_argument(
        "-f", "--fuzzy", action="store_true", help="print only files marked as fuzzys",
    )

    parser.add_argument(
        "-o",
        "--offline",
        action="store_true",
        help="don't perform any fetching to GitHub/online",
    )

    parser.add_argument(
        "-n",
        "--no-reserved",
        dest="hide_reserved",
        action="store_true",
        help="don't print info about reserved files",
    )

    parser.add_argument(
        "-c",
        "--counts",
        action="store_true",
        help="render list with the count of remaining entries "
        "(translate or review) rather than percentage done",
    )

    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        dest="json_format",
        help="format output as JSON.",
    )

    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__
    )

    args = parser.parse_args()

    # If no path is specified, use current directory
    if not args.path:
        args.path = os.getcwd()

    exec_potodo(**vars(args))
