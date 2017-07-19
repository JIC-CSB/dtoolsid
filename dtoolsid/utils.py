"""Utilities for dtoolsid."""


def is_file_extension_in_list(filename, extension_list):
    for extension in extension_list:
        if filename.endswith(extension):
            return True

    return False
