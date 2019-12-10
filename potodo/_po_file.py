import polib

from pathlib import Path


class PoFile:
    def __init__(self, path: Path):
        self.path: Path = path
        self.filename: str = path.name
        self.pofile: polib.POFile = polib.pofile(self.path)

        self.fuzzy_entries: list = self.pofile.fuzzy_entries()
        self.fuzzy_nb: int = len(self.fuzzy_entries)

        self.percent_translated: int = self.pofile.percent_translated()

        self.translated_entries: list = self.pofile.translated_entries()
        self.translated_nb: int = len(self.translated_entries)

        self.untranslated_entries: list = self.pofile.untranslated_entries()
        self.untranslated_nb: int = len(self.untranslated_entries)

    def __str__(self):
        return f"Filename: {self.filename}\nFuzzy Entries: {self.fuzzy_entries}\nPercent Translated: {self.percent_translated}\nTranslated Entries: {self.translated_entries}\nUntranslated Entries: {self.untranslated_entries}"


def get_po_files(path: str):
    po_files = [file for file in Path(path).glob("**/*.po") if ".git/" not in str(file)]
    po_files_per_directory = {
        path.parent.name: set(path.parent.glob("*.po")) for path in po_files
    }
    end_dict = {}
    for directory, po_files in sorted(po_files_per_directory.items()):
        new_list = []
        for po_file in po_files:
            new_list.append(PoFile(po_file))
        end_dict[directory] = new_list
    return end_dict
