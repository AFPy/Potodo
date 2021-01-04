import sys
from subprocess import check_output


def test_no_exclude(repo_dir):
    output = check_output(
        [sys.executable, "-m", "potodo", "-p", str(repo_dir)], universal_newlines=True
    )
    assert "file1" in output
    assert "file2" in output
    assert "file3" in output


def test_exclude_file(repo_dir):
    output = check_output(
        [sys.executable, "-m", "potodo", "--exclude", "file*", "-p", str(repo_dir)],
        universal_newlines=True,
    )
    assert "file1" not in output
    assert "file2" not in output
    assert "file3" not in output
    assert "excluded" in output  # The only one not being named file


def test_exclude_directory(repo_dir):
    output = check_output(
        [
            sys.executable,
            "-m",
            "potodo",
            "--exclude",
            "excluded/*",
            "-p",
            str(repo_dir),
        ],
        universal_newlines=True,
    )
    assert "file1" in output
    assert "file2" in output
    assert "file3" in output
    assert "file4" not in output  # in the excluded/ directory
    assert "excluded/" not in output


def test_exclude_single_file(repo_dir):
    output = check_output(
        [
            sys.executable,
            "-m",
            "potodo",
            "--exclude",
            "file2.po",
            "-p",
            str(repo_dir),
        ],
        universal_newlines=True,
    )
    assert "file1" in output
    assert "file2" not in output
    assert "file3" in output
    assert "file4" in output
