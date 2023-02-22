from pathlib import Path

import pytest


@pytest.fixture
def repo_dir():
    return Path(__file__).resolve().parent / "fixtures" / "repository"


@pytest.fixture
def base_config(repo_dir):
    return {
        "path": repo_dir,
        "exclude": ["excluded/", "excluded.po"],
        "above": 0,
        "below": 100,
        "only_fuzzy": False,
        "hide_reserved": False,
        "counts": False,
        "is_interactive": False,
        "exclude_fuzzy": False,
        "only_reserved": False,
        "exclude_reserved": False,
        "show_reservation_dates": False,
        "no_cache": True,
        "matching_files": False,
        "json_format": False,
        "api_url": "",
    }
