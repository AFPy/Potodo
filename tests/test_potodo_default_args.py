from pathlib import Path

from subprocess import check_output

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


class TestPotodoCLI:
    config = BASE_CONFIG
    excluded_1 = str(config["exclude"][0])
    excluded_2 = str(config["exclude"][1])

    def test_potodo_no_args(self):
        """
        Run test arguments.

        Args:
            self: (todo): write your description
        """
        output = check_output("potodo").decode("utf-8")
        assert "# excluded (50.00% done)" in output
        assert "# folder (33.33% done)" in output
        assert (
            "- excluded.po                      1 /   2 ( 50.0% translated)" in output
        )
        assert (
            "- file3.po                         0 /   1 (  0.0% translated)" in output
        )
        assert "# repository (25.00% done)" in output
        assert (
            "- file1.po                         1 /   3 ( 33.0% translated), 1 fuzzy"
            in output
        )

    def test_potodo_exclude(self):
        """
        Exclude an exclude to test.

        Args:
            self: (todo): write your description
        """
        output = check_output(
            ["potodo", "--exclude", self.excluded_1, self.excluded_2]
        ).decode("utf-8")
        output_short = check_output(
            ["potodo", "-e", self.excluded_1, self.excluded_2]
        ).decode("utf-8")
        assert output == output_short
        assert "# excluded (50.00% done)" not in output
        assert (
            "- excluded.po                      1 /   2 ( 50.0% translated)"
            not in output
        )
        assert "# repository (25.00% done)" in output
        assert (
            "- file1.po                         1 /   3 ( 33.0% translated), 1 fuzzy"
            in output
        )

    def test_potodo_above(self):
        """
        Test that the test is called.

        Args:
            self: (todo): write your description
        """
        output = check_output(["potodo", "--above", "40"]).decode("utf-8")
        output_short = check_output(["potodo", "-a", "40"]).decode("utf-8")
        assert output == output_short
        assert (
            "- file1.po                         1 /   3 ( 33.0% translated), 1 fuzzy"
            not in output
        )
        assert (
            "- excluded.po                      1 /   2 ( 50.0% translated)" in output
        )

    def test_potodo_below(self):
        """
        Test if the test was run.

        Args:
            self: (todo): write your description
        """
        output = check_output(["potodo", "--below", "40"]).decode("utf-8")
        output_short = check_output(["potodo", "-b", "40"]).decode("utf-8")
        assert output == output_short
        assert (
            "- file1.po                         1 /   3 ( 33.0% translated), 1 fuzzy"
            in output
        )
        assert (
            "- excluded.po                      1 /   2 ( 50.0% translated)"
            not in output
        )

    def test_potodo_onlyfuzzy(self):
        """
        Test if the test is enabled.

        Args:
            self: (todo): write your description
        """
        output = check_output(["potodo", "--only-fuzzy"]).decode("utf-8")
        output_short = check_output(["potodo", "-f"]).decode("utf-8")
        assert output == output_short
        assert (
            "- file1.po                         1 /   3 ( 33.0% translated), 1 fuzzy"
            in output
        )
        assert (
            "- excluded.po                      1 /   2 ( 50.0% translated)"
            not in output
        )

    def test_potodo_counts(self):
        """
        Determine whether the number of tests.

        Args:
            self: (todo): write your description
        """
        output = check_output(["potodo", "--counts"]).decode("utf-8")
        output_short = check_output(["potodo", "-c"]).decode("utf-8")
        assert output == output_short
        assert (
            "- excluded.po                      1 /   2 ( 50.0% translated)"
            not in output
        )
        assert "- file4.po                         1 to do" in output
        assert "# repository (25.00% done)" in output
        assert (
            "- file1.po                         2 to do, including 1 fuzzies." in output
        )

    def test_potodo_exclude_fuzzy(self):
        """
        Exclude test test test test.

        Args:
            self: (todo): write your description
        """
        output = check_output(["potodo", "--exclude-fuzzy"]).decode("utf-8")
        assert (
            "- excluded.po                      1 /   2 ( 50.0% translated)" in output
        )
        assert (
            "- file1.po                         2 to do, including 1 fuzzies."
            not in output
        )

    def test_potodo_matching_files_solo(self):
        """
        Check for potential files that match files.

        Args:
            self: (todo): write your description
        """
        output = check_output(["potodo", "--matching-files"]).decode("utf-8")
        output_short = check_output(["potodo", "-l"]).decode("utf-8")
        assert output == output_short
        assert "excluded/file4.po" in output
        assert "folder/excluded.po" in output
        assert "folder/file3.po" in output
        assert "file1.po" in output
        assert "file2.po" in output

    def test_potodo_matching_files_fuzzy(self):
        """
        Test whether the potential files that have the correct.

        Args:
            self: (todo): write your description
        """
        output = check_output(["potodo", "--matching-files", "--only-fuzzy"]).decode(
            "utf-8"
        )
        output_short = check_output(["potodo", "-l", "-f"]).decode("utf-8")
        assert output == output_short
        assert "file1.po" in output

    # TODO: Test hide_reserved, offline options, only_reserved, exclude_reserved, show_reservation_dates
    # TODO: Test verbose output levels
