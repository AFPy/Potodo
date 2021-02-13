import sys
from subprocess import check_output


class TestPotodoCLI:
    def test_potodo_no_args(self):
        output = check_output([sys.executable, "-m", "potodo"]).decode("utf-8")
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

    def test_potodo_exclude(self, base_config):
        output = check_output(
            [
                sys.executable,
                "-m",
                "potodo",
                "--exclude",
                base_config["exclude"][0],
                base_config["exclude"][1],
            ]
        ).decode("utf-8")
        output_short = check_output(
            [
                sys.executable,
                "-m",
                "potodo",
                "-e",
                base_config["exclude"][0],
                base_config["exclude"][1],
            ]
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
        output = check_output([sys.executable, "-m", "potodo", "--above", "40"]).decode(
            "utf-8"
        )
        output_short = check_output(
            [sys.executable, "-m", "potodo", "-a", "40"]
        ).decode("utf-8")
        assert output == output_short
        assert (
            "- file1.po                         1 /   3 ( 33.0% translated), 1 fuzzy"
            not in output
        )
        assert (
            "- excluded.po                      1 /   2 ( 50.0% translated)" in output
        )

    def test_potodo_below(self):
        output = check_output([sys.executable, "-m", "potodo", "--below", "40"]).decode(
            "utf-8"
        )
        output_short = check_output(
            [sys.executable, "-m", "potodo", "-b", "40"]
        ).decode("utf-8")
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
        output = check_output([sys.executable, "-m", "potodo", "--only-fuzzy"]).decode(
            "utf-8"
        )
        output_short = check_output([sys.executable, "-m", "potodo", "-f"]).decode(
            "utf-8"
        )
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
        output = check_output([sys.executable, "-m", "potodo", "--counts"]).decode(
            "utf-8"
        )
        output_short = check_output([sys.executable, "-m", "potodo", "-c"]).decode(
            "utf-8"
        )
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
        output = check_output(
            [sys.executable, "-m", "potodo", "--exclude-fuzzy"]
        ).decode("utf-8")
        assert (
            "- excluded.po                      1 /   2 ( 50.0% translated)" in output
        )
        assert (
            "- file1.po                         2 to do, including 1 fuzzies."
            not in output
        )

    def test_potodo_matching_files_solo(self):
        output = check_output(
            [sys.executable, "-m", "potodo", "--matching-files"]
        ).decode("utf-8")
        output_short = check_output([sys.executable, "-m", "potodo", "-l"]).decode(
            "utf-8"
        )
        assert output == output_short
        assert "excluded/file4.po" in output
        assert "folder/excluded.po" in output
        assert "folder/file3.po" in output
        assert "file1.po" in output
        assert "file2.po" in output

    def test_potodo_matching_files_fuzzy(self):
        output = check_output(
            [sys.executable, "-m", "potodo", "--matching-files", "--only-fuzzy"]
        ).decode("utf-8")
        output_short = check_output(
            [sys.executable, "-m", "potodo", "-l", "-f"]
        ).decode("utf-8")
        assert output == output_short
        assert "file1.po" in output

    # TODO: Test hide_reserved, offline options, only_reserved, exclude_reserved, show_reservation_dates
    # TODO: Test verbose output levels
