import sys
from pathlib import Path
from subprocess import check_output, CalledProcessError


class TestPotodoArgsErrors:
    def test_potodo_help(self):
        output = check_output([sys.executable, "-m", "potodo", "--help"]).decode(
            "utf-8"
        )
        output_short = check_output([sys.executable, "-m", "potodo", "-h"]).decode(
            "utf-8"
        )
        assert output == output_short
        assert "-h, --help            show this help message and exit" in output
        # TODO: Find a better way of testing help output

    def test_potodo_above_below_conflict(self):
        try:
            check_output(
                [sys.executable, "-m", "potodo", "--above", "50", "--below", "40"]
            ).decode("utf-8")
        except CalledProcessError as e:
            output = e.output
        try:
            check_output(
                [sys.executable, "-m", "potodo", "-a", "50", "-b", "40"]
            ).decode("utf-8")
        except CalledProcessError as e:
            output_short = e.output
        assert output == output_short
        assert output == b"Potodo: 'below' value must be greater than 'above' value.\n"

    def test_potodo_json_interactive_conflict(self):
        try:
            check_output(
                [sys.executable, "-m", "potodo", "--json", "--interactive"]
            ).decode("utf-8")
        except CalledProcessError as e:
            output = e.output
        try:
            check_output([sys.executable, "-m", "potodo", "-j", "-i"]).decode("utf-8")
        except CalledProcessError as e:
            output_short = e.output
        assert output == output_short
        assert (
            output
            == b"Potodo: Json format and interactive modes cannot be activated at the same time.\n"
        )

    def test_potodo_exclude_and_only_fuzzy_conflict(self):
        try:
            check_output(
                [sys.executable, "-m", "potodo", "--exclude-fuzzy", "--only-fuzzy"]
            ).decode("utf-8")
        except CalledProcessError as e:
            output = e.output
        assert (
            output
            == b"Potodo: Cannot pass --exclude-fuzzy and --only-fuzzy at the same time.\n"
        )

    def test_potodo_exclude_and_only_reserved_conflict(self):
        try:
            check_output(
                [
                    sys.executable,
                    "-m",
                    "potodo",
                    "--exclude-reserved",
                    "--only-reserved",
                ]
            ).decode("utf-8")
        except CalledProcessError as e:
            output = e.output
        assert (
            output
            == b"Potodo: Cannot pass --exclude-reserved and --only-reserved at the same time.\n"
        )
