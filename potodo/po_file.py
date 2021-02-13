import itertools
import logging
import os
from pathlib import Path
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Sequence
from typing import Set

import polib


class PoFileStats:
    """Class for each `.po` file containing all the necessary information about its progress"""  # noqa

    def __init__(self, path: Path):
        """Initializes the class with all the correct information"""
        self.path: Path = path
        self.filename: str = path.name
        self.mtime = os.path.getmtime(path)
        self.pofile: polib.POFile = polib.pofile(self.path)
        self.directory: str = self.path.parent.name

        self.obsolete_entries: Sequence[polib.POEntry] = self.pofile.obsolete_entries()
        self.obsolete_nb: int = len(self.pofile.obsolete_entries())

        self.fuzzy_entries: List[polib.POEntry] = [
            entry for entry in self.pofile if entry.fuzzy and not entry.obsolete
        ]
        self.fuzzy_nb: int = len(self.fuzzy_entries)

        self.translated_entries: Sequence[
            polib.POEntry
        ] = self.pofile.translated_entries()
        self.translated_nb: int = len(self.translated_entries)

        self.untranslated_entries: Sequence[
            polib.POEntry
        ] = self.pofile.untranslated_entries()
        self.untranslated_nb: int = len(self.untranslated_entries)

        self.entries_count: int = len([e for e in self.pofile if not e.obsolete])
        self.percent_translated: int = self.pofile.percent_translated()
        self.po_file_size = len(self.pofile) - self.obsolete_nb
        self.filename_dir: str = self.directory + "/" + self.filename

    def __str__(self) -> str:
        return (
            f"Filename: {self.filename}\n"
            f"Fuzzy Entries: {self.fuzzy_entries}\n"
            f"Percent Translated: {self.percent_translated}\n"
            f"Translated Entries: {self.translated_entries}\n"
            f"Untranslated Entries: {self.untranslated_entries}"
        )

    def __lt__(self, other: "PoFileStats") -> bool:
        """When two PoFiles are compared, their filenames are compared."""
        return self.filename < other.filename


from potodo.cache import get_cache_file_content  # noqa
from potodo.cache import set_cache_content  # noqa


def get_po_stats_from_repo_or_cache(
    repo_path: Path,
    ignore_matches: Callable[[str], bool],
    no_cache: bool = False,
) -> Mapping[str, List[PoFileStats]]:
    """Gets all the po files recursively from 'repo_path'
    and cache if no_cache is set to False, excluding those if ignore_matches match them.
    Return a dict with all directories and PoFile instances of
    `.po` files in those directories.
    """

    # Get all the files matching `**/*.po`
    # not being in the exclusion list or in
    # any (sub)folder from the exclusion list
    logging.debug("Finding all files matching **/*.po in %s", repo_path)
    all_po_files: List[Path] = [
        file for file in repo_path.rglob("*.po") if not ignore_matches(str(file))
    ]

    # Group files by directory
    logging.debug("Grouping files per directory")
    po_files_per_directory: Mapping[str, Set[Path]] = {
        name: set(files)
        # We assume the output of rglob to be sorted,
        # so each 'name' is unique within groupby
        for name, files in itertools.groupby(
            all_po_files, key=lambda path: path.parent.name
        )
    }

    if no_cache:
        # Turn paths into stat objects
        logging.debug("Creating PoFileStats objects for each file without cache")
        po_stats_per_directory: Dict[str, List[PoFileStats]] = {
            directory: [PoFileStats(po_file) for po_file in po_files]
            for directory, po_files in po_files_per_directory.items()
        }
    else:
        cached_files = get_cache_file_content(
            path=str(repo_path.resolve()) + "/.potodo/cache.pickle",
        )
        po_stats_per_directory = dict()
        for directory, po_files in po_files_per_directory.items():
            po_stats_per_directory[directory] = []
            for po_file in po_files:
                cached_file = cached_files.get(po_file.resolve())
                if not (
                    cached_file
                    and os.path.getmtime(po_file.resolve()) == cached_file.mtime
                ):
                    cached_files[po_file.resolve()] = cached_file = PoFileStats(po_file)
                po_stats_per_directory[directory].append(cached_file)
        set_cache_content(
            cached_files,
            path=str(repo_path.resolve()) + "/.potodo/cache.pickle",
        )

    return po_stats_per_directory
