from pathlib import Path
from typing import cast
from typing import Iterable
from typing import List
from typing import Callable

from simple_term_menu import TerminalMenu

from potodo.po_file import is_within

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


def get_dir_list(
    repo_path: Path, exclude: Iterable[Path], ignore_matches: Callable[[str], bool]
) -> List[str]:
    return list(
        set(
            [
                file.parent.name
                for file in repo_path.rglob("*.po")
                if not any(is_within(file, excluded) for excluded in exclude)
                and not ignore_matches(str(file))
            ]
        )
    )


def get_files_from_dir(
    directory: str, repo_path: Path, exclude: Iterable[Path]
) -> List[str]:
    path = Path(str(repo_path) + "/" + directory)
    return [
        file.name
        for file in path.rglob("*.po")
        if not any(is_within(file, excluded) for excluded in exclude)
    ]
