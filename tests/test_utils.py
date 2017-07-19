"""Test utils."""


def test_is_file_extension_in_list():

    from dtoolsid.utils import is_file_extension_in_list

    assert is_file_extension_in_list("foo.fq", ["fq"])
    assert not is_file_extension_in_list("foo.fq.gz", ["fq"])
    assert is_file_extension_in_list("foo.fq.gz", ["fq", "fq.gz"])
    assert is_file_extension_in_list("foo.clean.fq.gz", ["fq.gz"])

