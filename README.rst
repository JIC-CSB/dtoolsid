dtoolsid
========

Experimental command line for dtool functionality testing.

The name sid is borrowed from Debian's unstable branch (and hence from Toy Story!).

Installation
------------

To install dtoolsid using pip::

    $ pip install https://github.com/JIC-CSB/dtoolsid/archive/master.zip


To install dtoolsid from source::

    $ git clone https://github.com/JIC-CSB/dtoolsid.git
    $ cd dtoolsid
    $ python setup.py install

Usage
-----

As dtoolsid is a rapidly evolving experimental tool the easiest way to find out
about its usage is to make use of the ``--help`` option.

For example::

    $ dtoolsid --help 
    Usage: dtoolsid [OPTIONS] COMMAND [ARGS]...

    Options:
      --version  Show the version and exit.
      --help     Show this message and exit.

    Commands:
      collection
      dataset

Show that there are two subcommands available ``collection`` and ``dataset``.
To find out about the ``dataset`` subcommand one can use use the ``--help``
option again::

    $ dtoolsid dataset --help
    Usage: dtoolsid dataset [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      identifiers
      manifest
      paths
      summary
      verify

To find out about the ``dataset summary`` subcommand one can again use the
``--help`` option::

    $ dtoolsid dataset summary --help
    Usage: dtoolsid dataset summary [OPTIONS] [PATH]

      Echo a JSON summary of the dataset.

    Options:
      --help  Show this message and exit.

This tells you that the ``dtoolsid dataset summary`` command takes the
path to a dataset as its first and only argument and that it will echo
back a JSON string summarising the dataset.

::

    $ dtoolsid dataset summary path/to/my_dataset
    {
      "Name": "my_dataset",
      "Creator": "olssont",
      "Number of files": 2,
      "Total size": 722
    }
