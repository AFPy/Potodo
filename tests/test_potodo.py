import json
from pathlib import Path

from potodo.potodo import exec_potodo

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
REPO_DIR = "python-docs-fr"


def test_potodo(capsys):
    exec_potodo(
        path=FIXTURE_DIR / REPO_DIR,
        above=0,
        below=100,
        fuzzy=False,
        hide_reserved=False,
        counts=False,
        offline=True,
        json_format=False,
    )
    captured = capsys.readouterr()
    assert "file1.po" in captured.out
    assert "file2.po" in captured.out
    assert "# folder" in captured.out
    assert "file3.po" in captured.out
    assert "1 fuzzy" in captured.out
    assert "2 fuzzy" not in captured.out


def test_json_output(capsys):
    exec_potodo(
        path=FIXTURE_DIR / REPO_DIR,
        above=0,
        below=100,
        fuzzy=False,
        hide_reserved=False,
        counts=False,
        offline=True,
        json_format=True,
    )
    output = json.loads(capsys.readouterr().out)

    expected = [
        {
            "name": "folder/",
            "percent_translated": 0.0,
            "files": [
                {
                    "name": "folder/file3",
                    "path": str(FIXTURE_DIR / REPO_DIR / "folder" / "file3.po"),
                    "entries": 1,
                    "fuzzies": 0,
                    "translated": 0,
                    "percent_translated": 0,
                    "reserved_by": None,
                },
            ],
        },
        {
            "name": "python-docs-fr/",
            "percent_translated": 16.5,
            "files": [
                {
                    "name": "python-docs-fr/file1",
                    "path": str(FIXTURE_DIR / REPO_DIR / "file1.po"),
                    "entries": 3,
                    "fuzzies": 1,
                    "translated": 1,
                    "percent_translated": 33,
                    "reserved_by": None,
                },
                {
                    "name": "python-docs-fr/file2",
                    "path": str(FIXTURE_DIR / REPO_DIR / "file2.po"),
                    "entries": 1,
                    "fuzzies": 0,
                    "translated": 0,
                    "percent_translated": 0,
                    "reserved_by": None,
                },
            ],
        },
    ]

    assert expected == output
