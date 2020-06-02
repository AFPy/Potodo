import json
from pathlib import Path

from potodo.potodo import exec_potodo

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
REPO_DIR = "repository"


def test_txt_output(capsys):
    exec_potodo(
        path=FIXTURE_DIR / REPO_DIR,
        exclude=list(),
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


def test_output(capsys):
    exec_potodo(
        path=FIXTURE_DIR / REPO_DIR,
        exclude=["excluded"],
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
            "name": f"{REPO_DIR}/",
            "percent_translated": 16.5,
            "files": [
                {
                    "name": f"{REPO_DIR}/file1",
                    "path": str(FIXTURE_DIR / REPO_DIR / "file1.po"),
                    "entries": 3,
                    "fuzzies": 1,
                    "translated": 1,
                    "percent_translated": 33,
                    "reserved_by": None,
                },
                {
                    "name": f"{REPO_DIR}/file2",
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
