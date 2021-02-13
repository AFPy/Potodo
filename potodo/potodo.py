import argparse
import json
import logging
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Sequence
from typing import Tuple

from gitignore_parser import rule_from_pattern

from potodo import __version__
from potodo.arguments_handling import check_args
from potodo.github import get_issue_reservations
from potodo.json import json_dateconv
from potodo.logging import setup_logging
from potodo.po_file import get_po_stats_from_repo_or_cache
from potodo.po_file import PoFileStats


def print_dir_stats(
    directory_name: str,
    buffer: Sequence[str],
    folder_stats: Dict[str, int],
    printed_list: Sequence[bool],
) -> None:
    """This function prints the directory name, its stats and the buffer"""
    if True in printed_list:
        logging.debug("Printing directory %s", directory_name)
        # If at least one of the files isn't done then print the
        # folder stats and file(s) Each time a file is went over True
        # or False is placed in the printed_list list.  If False is
        # placed it means it doesnt need to be printed

        folder_completion = 100 * folder_stats["translated"] / folder_stats["total"]

        print(f"\n\n# {directory_name} ({folder_completion:.2f}% done)\n")
        print("\n".join(buffer))
    logging.debug("Not printing directory %s", directory_name)


def add_dir_stats(
    directory_name: str,
    buffer: List[Dict[str, str]],
    folder_stats: Dict[str, int],
    printed_list: Sequence[bool],
    all_stats: List[Dict[str, Any]],
) -> None:
    """Appends directory name, its stats and the buffer to stats"""
    if any(printed_list):
        folder_completion = 100 * folder_stats["translated"] / folder_stats["total"]
        all_stats.append(
            dict(
                name=f"{directory_name}/",
                percent_translated=float(f"{folder_completion:.2f}"),
                files=buffer,
            )
        )


def non_interactive_output(
    path: Path,
    exclude: List[str],
    above: int,
    below: int,
    only_fuzzy: bool,
    offline: bool,
    hide_reserved: bool,
    counts: bool,
    json_format: bool,
    exclude_fuzzy: bool,
    exclude_reserved: bool,
    only_reserved: bool,
    show_reservation_dates: bool,
    no_cache: bool,
    is_interactive: bool,
    matching_files: bool,
    ignore_matches: Callable[[str], bool],
) -> None:
    dir_stats: List[Any] = []
    # Initialize the arguments
    issue_reservations = get_issue_reservations(offline, hide_reserved, path)

    total_translated: int = 0
    total_entries: int = 0
    po_files_and_dirs = get_po_stats_from_repo_or_cache(path, ignore_matches, no_cache)
    for directory_name, po_files in sorted(po_files_and_dirs.items()):
        # For each directory and files in this directory
        buffer: List[Any] = []
        folder_stats: Dict[str, int] = {"translated": 0, "total": 0}
        printed_list: List[bool] = []

        for po_file in sorted(po_files):
            # For each file in those files from that directory
            if not only_fuzzy or po_file.fuzzy_entries:
                if exclude_fuzzy and po_file.fuzzy_entries:
                    continue
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
                    exclude_reserved,
                    only_reserved,
                    show_reservation_dates,
                    matching_files,
                )

        # Once all files have been processed, print the dir and the files
        # or store them into a dict to print them once all directories have
        # been processed.
        if json_format:
            add_dir_stats(directory_name, buffer, folder_stats, printed_list, dir_stats)
        else:
            print_dir_stats(directory_name, buffer, folder_stats, printed_list)

        total_translated += folder_stats["translated"]
        total_entries += folder_stats["total"]

    if json_format:
        print(
            json.dumps(
                dir_stats,
                indent=4,
                separators=(",", ": "),
                sort_keys=False,
                default=json_dateconv,
            )
        )
    else:
        if total_entries != 0:
            total_completion = 100 * total_translated / total_entries
            print(f"\n\n# TOTAL ({total_completion:.2f}% done)\n")


def build_ignore_matcher(path: Path, exclude: List[str]) -> Callable[[str], bool]:
    path = path.resolve()
    potodo_ignore = path / ".potodoignore"
    rules = []
    if potodo_ignore.exists():
        for line in potodo_ignore.read_text().splitlines():
            rule = rule_from_pattern(line, path)
            if rule:
                rules.append(rule)
    rules.append(rule_from_pattern(".git/", path))
    for rule in exclude:
        rules.append(rule_from_pattern(rule, path))
    return lambda file_path: any(r.match(file_path) for r in rules)


def exec_potodo(
    path: Path,
    exclude: List[str],
    above: int,
    below: int,
    only_fuzzy: bool,
    offline: bool,
    hide_reserved: bool,
    counts: bool,
    json_format: bool,
    exclude_fuzzy: bool,
    exclude_reserved: bool,
    only_reserved: bool,
    show_reservation_dates: bool,
    no_cache: bool,
    is_interactive: bool,
    matching_files: bool,
) -> None:
    """
    Will run everything based on the given parameters

    :param path: The path to search into
    :param exclude: folders or files to be ignored
    :param above: The above threshold
    :param below: The below threshold
    :param only_fuzzy: Should only fuzzies be printed
    :param offline: Will not connect to internet
    :param hide_reserved: Will not show the reserved files
    :param counts: Render list with counts not percentage
    :param json_format: Format output as JSON.
    :param exclude_fuzzy: Will exclude files with fuzzies in output.
    :param exclude_reserved: Will print out only files that aren't reserved
    :param only_reserved: Will print only reserved files
    :param show_reservation_dates: Will show the reservation dates
    :param no_cache: Disables cache (Cache is disabled when files are modified)
    :param is_interactive: Switches output to an interactive CLI menu
    :param matching_files: Should the file paths be printed instead of normal output
    """

    ignore_matches = build_ignore_matcher(path, exclude)
    if is_interactive:
        from potodo.interactive import interactive_output

        interactive_output(path, ignore_matches)
    else:
        non_interactive_output(
            path,
            exclude,
            above,
            below,
            only_fuzzy,
            offline,
            hide_reserved,
            counts,
            json_format,
            exclude_fuzzy,
            exclude_reserved,
            only_reserved,
            show_reservation_dates,
            no_cache,
            is_interactive,
            matching_files,
            ignore_matches,
        )


def buffer_add(
    buffer: List[Any],
    folder_stats: Dict[str, int],
    printed_list: List[bool],
    po_file_stats: PoFileStats,
    issue_reservations: Dict[str, Tuple[Any, Any]],
    above: int,
    below: int,
    counts: bool,
    json_format: bool,
    exclude_reserved: bool,
    only_reserved: bool,
    show_reservation_dates: bool,
    matching_files: bool,
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
        folder_stats["translated"] += po_file_stats.translated_nb
        folder_stats["total"] += po_file_stats.entries_count

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
    reserved_by, reservation_date = issue_reservations.get(
        po_file_stats.filename_dir.lower(), (None, None)
    )
    # unless the offline/hide_reservation are enabled
    if exclude_reserved and reserved_by:
        return
    if only_reserved and not reserved_by:
        return

    directory = po_file_stats.directory
    filename = po_file_stats.filename
    path = po_file_stats.path

    if matching_files:
        print(path)
        return
    elif json_format:

        # the order of the keys is the display order
        d = dict(
            name=f"{directory}/{filename.replace('.po', '')}",
            path=str(path),
            entries=po_file_size,
            fuzzies=fuzzy_nb,
            translated=translated_nb,
            percent_translated=percent_translated,
            reserved_by=reserved_by,
            reservation_date=reservation_date,
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
            if show_reservation_dates:
                s += f" ({reservation_date})"

        buffer.append(s)

    # Add the percent translated to the folder statistics
    folder_stats["translated"] += po_file_stats.translated_nb
    folder_stats["total"] += po_file_stats.entries_count
    # Indicate to print the file
    printed_list.append(True)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="potodo",
        description="List and prettify the po files left to translate.",
    )

    parser.add_argument(
        "-p",
        "--path",
        help="execute Potodo in path",
        metavar="path",
    )

    parser.add_argument(
        "-e",
        "--exclude",
        nargs="+",
        default=[],
        help="gitignore-style patterns to exclude from search.",
        metavar="path",
    )

    parser.add_argument(
        "-a",
        "--above",
        default=0,
        metavar="X",
        type=int,
        help="list all TODOs above given X%% completion",
    )

    parser.add_argument(
        "-b",
        "--below",
        default=100,
        metavar="X",
        type=int,
        help="list all TODOs below given X%% completion",
    )

    parser.add_argument(
        "-f",
        "--only-fuzzy",
        dest="only_fuzzy",
        action="store_true",
        help="print only files marked as fuzzys",
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
        help="format output as JSON",
    )

    parser.add_argument(
        "--exclude-fuzzy",
        action="store_true",
        dest="exclude_fuzzy",
        help="select only files without fuzzy entries",
    )

    parser.add_argument(
        "--exclude-reserved",
        action="store_true",
        dest="exclude_reserved",
        help="select only files that aren't reserved",
    )

    parser.add_argument(
        "--only-reserved",
        action="store_true",
        dest="only_reserved",
        help="select only only reserved files",
    )

    parser.add_argument(
        "--show-reservation-dates",
        action="store_true",
        dest="show_reservation_dates",
        help="show issue creation dates",
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        dest="no_cache",
        help="Disables cache (Cache is disabled when files are modified)",
    )

    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        dest="is_interactive",
        help="Activates the interactive menu",
    )

    parser.add_argument(
        "-l",
        "--matching-files",
        action="store_true",
        dest="matching_files",
        help="Suppress normal output; instead print the name of each matching po file from which output would normally "
        "have been printed.",
    )

    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__
    )

    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increases output verbosity"
    )

    # Initialize args and check consistency
    args = vars(parser.parse_args())
    args.update(check_args(**args))

    if args["logging_level"]:
        setup_logging(args["logging_level"])

    logging.info("Logging activated.")
    logging.debug("Executing potodo with args %s", args)

    # Removing useless args before running the process
    del args["verbose"]
    del args["logging_level"]

    # Launch the processing itself
    exec_potodo(**args)
