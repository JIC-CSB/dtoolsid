"""Test the dtoolsid dataset CLI tool."""

import os
import subprocess

from . import dataset_fixture  # NOQA


def test_version():
    cmd = ["dtoolsid", "--version"]
    version = subprocess.check_output(cmd).decode("utf-8")
    assert version.startswith("dtoolsid, version")


def test_dataset_identifiers(dataset_fixture):  # NOQA
    cmd = ["dtoolsid", "dataset", "identifiers", dataset_fixture]
    identifiers = subprocess.check_output(cmd).decode("utf-8")
    assert len(identifiers.split()) == 2


def test_dataset_paths(dataset_fixture):  # NOQA
    cmd = ["dtoolsid", "dataset", "paths", dataset_fixture]
    output_string = subprocess.check_output(cmd).decode("utf-8")
    paths = output_string.split()
    assert len(paths) == 2
    for path in paths:
        assert os.path.isfile(path)


def test_dataset_manifest(dataset_fixture):  # NOQA
    import json
    import dtoolcore
    cmd = ["dtoolsid", "dataset", "manifest", dataset_fixture]
    manifest_str = subprocess.check_output(cmd).decode("utf-8")
    manifest = json.loads(manifest_str)
    dataset = dtoolcore.DataSet.from_path(dataset_fixture)
    assert manifest == dataset.manifest


def test_dataset_summary(dataset_fixture):  # NOQA
    import json
    import getpass
    cmd = ["dtoolsid", "dataset", "summary", dataset_fixture]
    summary_str = subprocess.check_output(cmd).decode("utf-8")
    summary = json.loads(summary_str)
    expected = {
        "Name": "test",
        "Creator": getpass.getuser(),
        "Number of files": 2,
        "Total size": 10,
    }
    assert summary == expected


def test_dataset_verify(dataset_fixture):  # NOQA
    import dtoolcore

    cmd = ["dtoolsid", "dataset", "verify", dataset_fixture]
    message_str = subprocess.check_output(cmd).decode("utf-8")
    assert message_str.strip() == "All good :)"

    # Add a unknown file to the data directory.
    fpath = os.path.join(dataset_fixture, "data", "unknown.txt")
    with open(fpath, "w") as fh:
        fh.write("this file is not indexed")

    message_str = subprocess.check_output(cmd).decode("utf-8")
    assert message_str.strip() == "Unknown file: {}".format(fpath)

    os.unlink(fpath)

    # Remove an indexed file.
    dataset = dtoolcore.DataSet.from_path(dataset_fixture)
    identifier = dataset.manifest["file_list"][0]["hash"]
    fpath = dataset.abspath_from_identifier(identifier)
    os.unlink(fpath)

    message_str = subprocess.check_output(cmd).decode("utf-8")
    assert message_str.strip() == "Missing file: {}".format(fpath)

    # Alter the content of an indexed file.
    with open(fpath, "w") as fh:
        fh.write("different content")
    message_str = subprocess.check_output(cmd).decode("utf-8")
    assert message_str.strip() == "Altered file: {}".format(fpath)
