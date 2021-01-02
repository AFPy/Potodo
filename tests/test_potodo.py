import json
from pathlib import Path

from potodo.potodo import exec_potodo

REPO_DIR = "repository"
ABS_REPO_DIR = Path(__file__).resolve().parent / "fixtures" / REPO_DIR

config = {
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
    "matching_files": False,
}


def test_txt_output(capsys):
    exec_potodo(json_format=False, **config)
    captured = capsys.readouterr()

    assert "# repository" in captured.out
    assert "file1.po" in captured.out
    assert "file2.po" in captured.out
    assert "# folder" in captured.out
    assert "file3.po" in captured.out
    assert "1 fuzzy" in captured.out
    assert "2 fuzzy" not in captured.out
    assert "excluded" not in captured.out
    assert "# TOTAL" in captured.out


def test_output(capsys):
    exec_potodo(json_format=True, **config)
    output = json.loads(capsys.readouterr().out)

    expected = [
        {
            "name": "folder/",
            "percent_translated": 0.0,
            "entries": 1,
            "fuzzies": 0,
            "translated": 0,
            "files": [
                {
                    "name": "folder/file3",
                    "path": f"{ABS_REPO_DIR}/folder/file3.po",
                    "entries": 1,
                    "fuzzies": 0,
                    "translated": 0,
                    "percent_translated": 0,
                    "reserved_by": None,
                    "reservation_date": None,
                },
            ],
        },
        {
            "name": f"{REPO_DIR}/",
            "percent_translated": 25.0,
            "entries": 4,
            "fuzzies": 1,
            "translated": 1,
            "files": [
                {
                    "name": f"{REPO_DIR}/file1",
                    "path": f"{ABS_REPO_DIR}/file1.po",
                    "entries": 3,
                    "fuzzies": 1,
                    "translated": 1,
                    "percent_translated": 33,
                    "reserved_by": None,
                    "reservation_date": None,
                },
                {
                    "name": f"{REPO_DIR}/file2",
                    "path": f"{ABS_REPO_DIR}/file2.po",
                    "entries": 1,
                    "fuzzies": 0,
                    "translated": 0,
                    "percent_translated": 0,
                    "reserved_by": None,
                    "reservation_date": None,
                },
            ],
        },
    ]

    assert output == expected
