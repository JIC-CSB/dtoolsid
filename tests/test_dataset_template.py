"""Test the dtoolsid dataset CLI tool."""

import os
import subprocess

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