from pathlib import Path
from fnmatch import fnmatch


def get_ignore_content(repo_path: Path, file=".potodoignore"):
    file_path = repo_path / file
    if not file_path.exists():
        return []
    with open(file_path, "r") as handle:
        lines = handle.readlines()
    ignore_pattern_set = set(lines)
    excluded_path_list = []
    for path in repo_path.rglob('*'):
        if path.is_file() and path != file_path:
            for ignore_pattern in ignore_pattern_set:
                relative_path = path.relative_to(repo_path)
                if fnmatch(relative_path, ignore_pattern):
                    # add in excludd list
                    excluded_path_list.append(path)
    return excluded_path_list

