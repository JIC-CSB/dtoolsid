"""Test the dtoolsid dataset CLI tool."""

import os
import subprocess

import yaml

from . import tmp_dir_fixture, ILLUMINA_DATASET_PATH  # NOQA


def test_dataset_template(tmp_dir_fixture):  # NOQA
    import dtoolcore

    template_dataset_directory = os.path.join(tmp_dir_fixture, "templ")
    cmd = [
        "dtoolsid",
        "dataset",
        "template",
        ILLUMINA_DATASET_PATH,
        template_dataset_directory,
    ]
    message_str = subprocess.check_output(cmd).decode("utf-8")

    templated_dataset = dtoolcore.DataSet.from_path(
        template_dataset_directory)
    with open(templated_dataset.abs_readme_path) as fh:
        templated_manifest = yaml.load(fh)

    assert templated_manifest["dataset_name"] == "templ"

    parent_dataset = dtoolcore.DataSet.from_path(ILLUMINA_DATASET_PATH)
    with open(parent_dataset.abs_readme_path) as fh:
        parent_manifest = yaml.load(fh)

    for key, value in parent_manifest.items():
        if key in ["dataset_name",]:
            continue
        assert templated_manifest[key] == value

