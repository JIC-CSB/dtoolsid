"""Test the dtoolsid package."""


def test_version_is_string():
    import dtoolsid
    assert isinstance(dtoolsid.__version__, str)
