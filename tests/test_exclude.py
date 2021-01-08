from potodo.potodo import exec_potodo


def test_no_exclude(capsys, base_config):
    exec_potodo(**base_config)
    out, err = capsys.readouterr()
    assert not err
    assert "file1" in out
    assert "file2" in out
    assert "file3" in out


def test_exclude_file(capsys, base_config):
    base_config["exclude"] = ["file*"]
    exec_potodo(**base_config)
    out, err = capsys.readouterr()
    assert not err
    assert "file1" not in out
    assert "file2" not in out
    assert "file3" not in out
    assert "excluded" in out  # The only one not being named file


def test_exclude_directory(capsys, base_config):
    base_config["exclude"] = ["excluded/*"]
    exec_potodo(**base_config)
    out, err = capsys.readouterr()
    assert not err
    assert "file1" in out
    assert "file2" in out
    assert "file3" in out
    assert "file4" not in out  # in the excluded/ directory
    assert "excluded/" not in out


def test_exclude_single_file(capsys, base_config):
    base_config["exclude"] = ["file2.po"]
    exec_potodo(**base_config)
    out, err = capsys.readouterr()
    assert not err
    assert "file1" in out
    assert "file2" not in out
    assert "file3" in out
    assert "file4" in out
