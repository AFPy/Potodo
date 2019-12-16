from pathlib import Path

from potodo.potodo import exec_potodo


FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def test_potodo(capsys):
    exec_potodo(
        path=FIXTURE_DIR / "python-docs-fr",
        above=0,
        below=100,
        fuzzy=False,
        hide_reserved=False,
        counts=False,
        offline=True,
        json_format=False,
    )
    captured = capsys.readouterr()
    assert "bugs.po" in captured.out
    assert "# library" in captured.out
    assert "token.po" in captured.out
    assert "glossary.po" not in captured.out
    assert "sphinx.po" not in captured.out
    assert "2 fuzzy" not in captured.out
    assert "3 fuzzy" in captured.out
