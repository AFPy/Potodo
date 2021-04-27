import json

from potodo.potodo import exec_potodo


def test_txt_output(capsys, base_config):
    exec_potodo(**base_config)
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


def test_output(capsys, base_config, repo_dir):
    base_config["json_format"] = True
    exec_potodo(**base_config)
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
                    "path": f"{repo_dir}/folder/file3.po",
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
            "name": "repository/",
            "percent_translated": 25.0,
            "entries": 4,
            "fuzzies": 1,
            "translated": 1,
            "files": [
                {
                    "name": "repository/file1",
                    "path": f"{repo_dir}/file1.po",
                    "entries": 3,
                    "fuzzies": 1,
                    "translated": 1,
                    "percent_translated": 33,
                    "reserved_by": None,
                    "reservation_date": None,
                },
                {
                    "name": "repository/file2",
                    "path": f"{repo_dir}/file2.po",
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
