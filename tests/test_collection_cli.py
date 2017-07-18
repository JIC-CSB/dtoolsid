"""Test the dtoolsid project CLI tool."""

import subprocess

from . import collection_fixture  # NOQA


def test_collection_summary(collection_fixture):  # NOQA
    import json
    cmd = ["dtoolsid", "collection", "summary", collection_fixture]
    summary_str = subprocess.check_output(cmd).decode("utf-8")
    summary = json.loads(summary_str)
    expected = {
        "Number of datasets": 3,
        "Number of files": 9,
        "Total size": 105,
    }
    assert summary == expected
