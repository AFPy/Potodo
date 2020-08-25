from simple_term_menu import TerminalMenu
from typing import List, Sequence
from potodo._po_file import PoFileStats


IS_CURSOR_CYCLING = True
IS_SCREEN_CLEARED = True


# TODO: Add go back and quit options

def _directory_list_menu(directory_list: List[str], excluded: List[str] = list):
    # TODO: Think about and do the exclusions
    # final_dir_list = [directory for directory in directory_list if directory not in excluded]
    final_dir_list = directory_list
    directory_list_menu = TerminalMenu(
        menu_entries=final_dir_list,
        title="Choose a directory",
        cycle_cursor=IS_CURSOR_CYCLING,
        clear_screen=IS_SCREEN_CLEARED,
        # preview_command="",
        # preview_size=0,
    )
    selected_directory = directory_list_menu.show()
    return selected_directory


# TODO: Think about and do the exclusions
def _file_list_menu(directory: str, file_list: Sequence[PoFileStats], excluded: List[str] = list):
    # final_file_list = [file.filename for file in file_list if file not in excluded]
    final_file_list = [file.filename for file in file_list]
    file_list_menu = TerminalMenu(
        menu_entries=final_file_list,
        title=f"Choose a file from {directory}",
        cycle_cursor=IS_CURSOR_CYCLING,
        clear_screen=IS_SCREEN_CLEARED,
        # preview_command="",
        # preview_size=0,
    )
    selected_file = file_list_menu.show()
    return selected_file


def _confirmation_menu(choosen_file: str, directory: str):
    confimation_menu = TerminalMenu(
        title=f"Are you sure you want to choose {directory}/{choosen_file}?"
              f" (This will open a web browser tab to open a new issue)",
        menu_entries=["YES", "NO"],
        cycle_cursor=IS_CURSOR_CYCLING,
        clear_screen=IS_SCREEN_CLEARED,
    )
    choice = confimation_menu.show()
    return choice
