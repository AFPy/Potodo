from typing import Dict, Mapping, Sequence, Set, List
from pathlib import Path

import polib


class PoFileStats:
    """Class for each `.po` file containing all the necessary information about its progress
    """

    def __init__(self, path: Path):
        """Initializes the class with all the correct information
        """
        self.path: Path = path
        self.filename: str = path.name
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
        """When two PoFiles are compared, their filenames are compared.
        """
        return self.filename < other.filename


def get_po_files_from_repo(repo_path: str) -> Mapping[str, Sequence[PoFileStats]]:
    """Gets all the po files from a given repository.  Will return a list
    with all directories and PoFile instances of `.po` files in those
    directories.
    """

    # Get all the files matching `**/*.po` and not being `.git/` in the given path
    all_po_files: Sequence[Path] = [
        file for file in Path(repo_path).glob("**/*.po") if ".git/" not in str(file)
    ]

    # Separates each directory and places all pofiles for each directory accordingly
    po_files_per_directory: Mapping[str, Set[Path]] = {
        path.parent.name: set(path.parent.glob("*.po")) for path in all_po_files
    }
    end_dict: Dict[str, Sequence[PoFileStats]] = {}
    for directory, po_files in sorted(po_files_per_directory.items()):
        # For each file in each directory, gets a PoFile instance then add it to a dict
        end_dict[directory] = [PoFileStats(po_file) for po_file in po_files]
    return end_dict
