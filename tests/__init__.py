"""Test fixtures."""

import os
import shutil
import tempfile

import pytest

import dtoolcore


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

    return dtoolcore.DataSet.from_path(subd)


@pytest.fixture
def tmp_illumina_dataset_directory(request):
    d = tempfile.mkdtemp()

    subd = os.path.join(d, 'sub')

    shutil.copytree(ILLUMINA_DATASET_PATH, subd)

    @request.addfinalizer
    def teatdown():
        shutil.rmtree(d)

    return subd


@pytest.fixture
def dataset_fixture(request):
    d = tempfile.mkdtemp()

    dataset = dtoolcore.DataSet("test", "data")
    dataset.persist_to_path(d)

    for s in ["hello", "world"]:
        fname = s + ".txt"
        fpath = os.path.join(d, "data", fname)
        with open(fpath, "w") as fh:
            fh.write(s)

    dataset.update_manifest()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return d


@pytest.fixture
def collection_fixture(request):
    collection_path = tempfile.mkdtemp()

    collection = dtoolcore.Collection()
    collection.persist_to_path(collection_path)

    for ds_name in ["rice", "wheat", "barley"]:

        ds_path = os.path.join(collection_path, ds_name)
        os.mkdir(ds_path)

        dataset = dtoolcore.DataSet(ds_name, "data")
        dataset.persist_to_path(ds_path)

        for s in ["sow", "grow", "harvest"]:
            fname = s + ".txt"
            fpath = os.path.join(ds_path, "data", fname)
            with open(fpath, "w") as fh:
                fh.write("{} {}\n".format(s, ds_name))

        dataset.update_manifest()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(collection_path)
    return collection_path
