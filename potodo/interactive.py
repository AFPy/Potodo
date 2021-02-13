import webbrowser
from pathlib import Path
from typing import Callable
from typing import cast
from typing import List

from simple_term_menu import TerminalMenu

IS_CURSOR_CYCLING = True
IS_SCREEN_CLEARED = True


def _directory_list_menu(directory_list: List[str]) -> int:
    final_dir_list = directory_list
    if "[q] Quit" not in final_dir_list:
        final_dir_list.append("[q] Quit")
    directory_list_menu = TerminalMenu(
        menu_entries=final_dir_list,
        title="Choose a directory",
        cycle_cursor=IS_CURSOR_CYCLING,
        clear_screen=IS_SCREEN_CLEARED,
        # preview_command="",
        # preview_size=0,
        show_search_hint=True,
        show_shortcut_hints=True,
    )
    selected_directory = directory_list_menu.show()
    return cast(int, selected_directory)


def _file_list_menu(directory: str, file_list: List[str]) -> int:
    if "[;] Back" not in file_list:
        file_list.append("[;] Back")
        file_list.append("[q] Quit")
    file_list_menu = TerminalMenu(
        menu_entries=file_list,
        title=f"Choose a file from {directory}",
        cycle_cursor=IS_CURSOR_CYCLING,
        clear_screen=IS_SCREEN_CLEARED,
        # preview_command="",
        # preview_size=0,
        show_search_hint=True,
        show_shortcut_hints=True,
    )
    selected_file = file_list_menu.show()
    return cast(int, selected_file)


def _confirmation_menu(choosen_file: str, directory: str) -> int:
    confimation_menu = TerminalMenu(
        title=f"Are you sure you want to choose {directory}/{choosen_file}?"
        f" (This will open a web browser tab to open a new issue)",
        menu_entries=["YES", "NO", "[;] Back", "[q] Quit"],
        cycle_cursor=IS_CURSOR_CYCLING,
        clear_screen=IS_SCREEN_CLEARED,
        show_search_hint=True,
        show_shortcut_hints=True,
    )
    choice = confimation_menu.show()
    return cast(int, choice)


def get_dir_list(repo_path: Path, ignore_matches: Callable[[str], bool]) -> List[str]:
    return list(
        set(
            [
                file.parent.name
                for file in repo_path.rglob("*.po")
                if not ignore_matches(str(file))
            ]
        )
    )


def get_files_from_dir(
    directory: str, repo_path: Path, ignore_matches: Callable[[str], bool]
) -> List[str]:
    path = Path(str(repo_path) + "/" + directory)
    return [file.name for file in path.rglob("*.po") if not ignore_matches(str(file))]


def interactive_output(path: Path, ignore_matches: Callable[[str], bool]) -> None:
    directory_options = get_dir_list(repo_path=path, ignore_matches=ignore_matches)
    while True:
        selected_dir = _directory_list_menu(directory_options)
        if selected_dir == (len(directory_options) - 1):
            exit(0)
        directory = directory_options[selected_dir]
        file_options = get_files_from_dir(
            directory=directory, repo_path=path, ignore_matches=ignore_matches
        )
        # TODO: Add stats on files and also add reservations
        selected_file = _file_list_menu(directory, file_options)
        if selected_file == (len(file_options) + 1):
            exit(0)
        elif selected_file == len(file_options):
            continue
        file = file_options[selected_file]
        final_choice = _confirmation_menu(file, directory)
        if final_choice == 3:
            exit(0)
        elif final_choice == 2:
            continue
        else:
            break
    if final_choice == 0:
        webbrowser.open(
            f"https://github.com/python/python-docs-fr/issues/new?title=Je%20travaille%20sur%20"
            f"{directory}/{file}"
            f"&body=%0A%0A%0A---%0AThis+issue+was+created+using+potodo+interactive+mode."
        )
    else:
        exit()
