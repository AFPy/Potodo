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

        self.obsolete_entries: list = self.pofile.obsolete_entries()
        self.obsolete_nb: int = len(self.pofile.obsolete_entries())

        self.po_file_size = len(self.pofile) - self.obsolete_nb

    def get_dir_and_filename(self, directory):
        return directory + "/" + self.filename

    def __str__(self):
        return f"Filename: {self.filename}\n" \
               f"Fuzzy Entries: {self.fuzzy_entries}\n" \
               f"Percent Translated: {self.percent_translated}\n" \
               f"Translated Entries: {self.translated_entries}\n" \
               f"Untranslated Entries: {self.untranslated_entries}"

    def __lt__(self, other):
        return self.filename < other.filename

def get_po_files_from_repo(repo_path: str):
    all_po_files = [file for file in Path(repo_path).glob("**/*.po") if ".git/" not in str(file)]
    po_files_per_directory = {
        path.parent.name: set(path.parent.glob("*.po")) for path in all_po_files
    }
    end_dict = {}
    for directory, po_files in sorted(po_files_per_directory.items()):
        new_list = []
        for po_file in po_files:
            new_list.append(PoFile(po_file))
        end_dict[directory] = new_list
    return end_dict
