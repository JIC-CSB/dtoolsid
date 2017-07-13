"""Test fixtures."""

import os
import shutil
import tempfile

import pytest

from dtool import DataSet

_HERE = os.path.dirname(__file__)
ILLUMINA_DATASET_PATH = os.path.join(_HERE, 'data', 'illumina_test_data')


@pytest.fixture
def chdir_fixture(request):
    d = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(d)

    @request.addfinalizer
    def teardown():
        os.chdir(curdir)
        shutil.rmtree(d)


@pytest.fixture
def tmp_dir_fixture(request):
    d = tempfile.mkdtemp()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return d


@pytest.fixture
def local_tmp_dir_fixture(request):
    d = tempfile.mkdtemp(dir=_HERE)

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return d


@pytest.fixture
def tmp_illumina_dataset(request):
    d = tempfile.mkdtemp()

    subd = os.path.join(d, 'sub')

    shutil.copytree(ILLUMINA_DATASET_PATH, subd)

    @request.addfinalizer
    def teatdown():
        shutil.rmtree(d)

    return DataSet.from_path(subd)
