from pathlib import Path

from subprocess import check_output, CalledProcessError

REPO_DIR = "repository"
ABS_REPO_DIR = Path(__file__).resolve().parent / "fixtures" / REPO_DIR

BASE_CONFIG = {
    "path": ABS_REPO_DIR,
    "exclude": [ABS_REPO_DIR / "excluded", ABS_REPO_DIR / "folder" / "excluded.po"],
    "above": 0,
    "below": 100,
    "only_fuzzy": False,
    "hide_reserved": False,
    "counts": False,
    "offline": True,
    "is_interactive": False,
    "exclude_fuzzy": False,
    "only_reserved": False,
    "exclude_reserved": False,
    "show_reservation_dates": False,
    "no_cache": True,
}


class TestPotodoArgsErrors:
    config = BASE_CONFIG
    excluded_1 = str(config["exclude"][0])
    excluded_2 = str(config["exclude"][1])

    def test_potodo_help(self):
        output = check_output(["potodo", "--help"]).decode("utf-8")
        output_short = check_output(["potodo", "-h"]).decode("utf-8")
        assert output == output_short
        assert "-h, --help            show this help message and exit" in output
        # TODO: Find a better way of testing help output

    def test_potodo_above_below_conflict(self):
        try:
            check_output(["potodo", "--above", "50", "--below", "40"]).decode("utf-8")
        except CalledProcessError as e:
            output = e.output
        try:
            check_output(["potodo", "-a", "50", "-b", "40"]).decode("utf-8")
        except CalledProcessError as e:
            output_short = e.output
        assert output == output_short
        assert output == b"Potodo: 'below' value must be greater than 'above' value.\n"

    def test_potodo_json_interactive_conflict(self):
        try:
            check_output(["potodo", "--json", "--interactive"]).decode("utf-8")
        except CalledProcessError as e:
            output = e.output
        try:
            check_output(["potodo", "-j", "-i"]).decode("utf-8")
        except CalledProcessError as e:
            output_short = e.output
        assert output == output_short
        assert (
            output
            == b"Potodo: Json format and interactive modes cannot be activated at the same time.\n"
        )

    def test_potodo_exclude_and_only_fuzzy_conflict(self):
        try:
            check_output(["potodo", "--exclude-fuzzy", "--only-fuzzy"]).decode("utf-8")
        except CalledProcessError as e:
            output = e.output
        assert (
            output
            == b"Potodo: Cannot pass --exclude-fuzzy and --only-fuzzy at the same time.\n"
        )

    def test_potodo_exclude_and_only_reserved_conflict(self):
        try:
            check_output(["potodo", "--exclude-reserved", "--only-reserved"]).decode(
                "utf-8"
            )
        except CalledProcessError as e:
            output = e.output
        assert (
            output
            == b"Potodo: Cannot pass --exclude-reserved and --only-reserved at the same time.\n"
        )

    def test_potodo_exclude_uknown_path(self):
        try:
            check_output(["potodo", "--exclude", "c-api"]).decode("utf-8")
        except CalledProcessError as e:
            output = e.output
        assert b"c-api` doesn't exist.\n" in output
