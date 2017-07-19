"""datademo command line tool."""

import os
import json

import click
import dtoolcore
import pygments
import pygments.lexers
import pygments.formatters

from dtoolsid import __version__

dataset_path_option = click.argument(
    'path',
    type=click.Path(exists=True))

collection_path_option = click.argument(
    'path',
    type=click.Path(exists=True))


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


#############################################################################
# datademo dataset
#############################################################################

@cli.group()
def dataset():
    pass


@dataset.command()
@dataset_path_option
def identifiers(path,):
    """Echo the identifiers in the dataset."""
    dataset = dtoolcore.DataSet.from_path(path)
    click.secho("\n".join(dataset.identifiers))


@dataset.command()
@dataset_path_option
def paths(path):
    """Echo the paths to the files in the dataset."""
    dataset = dtoolcore.DataSet.from_path(path)

    paths = [dataset.abspath_from_identifier(identifier)
             for identifier in dataset.identifiers]

    click.secho('\n'.join(paths))


@dataset.command()
@dataset_path_option
def manifest(path):
    """Echo the JSON manifest file."""
    dataset = dtoolcore.DataSet.from_path(path)
    formatted_json = json.dumps(dataset.manifest, indent=2)
    colorful_json = pygments.highlight(
        formatted_json,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter())
    click.secho(colorful_json, nl=False)


@dataset.command()
@dataset_path_option
def summary(path):
    """Echo a JSON summary of the dataset."""
    dataset = dtoolcore.DataSet.from_path(path)
    file_list = dataset.manifest["file_list"]
    total_size = sum([f["size"] for f in file_list])

    json_lines = [
        "{",
        '  "Name": "{}",'.format(dataset.name),
        '  "Creator": "{}",'.format(dataset.creator_username),
        '  "Number of files": {},'.format(len(file_list)),
        '  "Total size": {}'.format(total_size),
        "}",
    ]
    formatted_json = "\n".join(json_lines)
    colorful_json = pygments.highlight(
        formatted_json,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter())
    click.secho(colorful_json, nl=False)


@dataset.command()
@dataset_path_option
def verify(path):
    """Verify the integrity of the dataset."""
    all_good = True
    dataset = dtoolcore.DataSet.from_path(path)
    manifest_data_paths = []
    for i in dataset.identifiers:
        fpath = dataset.abspath_from_identifier(i)
        manifest_data_paths.append(fpath)
        if not os.path.isfile(fpath):
            click.secho("Missing file: {}".format(fpath), fg="red")
            all_good = False
            continue
        calculated_hash = dataset._structural_metadata.hash_generator(fpath)
        if i != calculated_hash:
            click.secho("Altered file: {}".format(fpath), fg="red")
            all_good = False
            continue

    abs_data_directory = os.path.join(path, dataset.data_directory)
    existing_data_paths = []
    for root, dirs, files in os.walk(abs_data_directory):
        for f in files:
            fpath = os.path.abspath(os.path.join(root, f))
            existing_data_paths.append(fpath)
    new_data_fpaths = set(existing_data_paths) - set(manifest_data_paths)
    for fpath in new_data_fpaths:
        all_good = False
        click.secho("Unknown file: {}".format(fpath), fg="yellow")

    if all_good:
        click.secho("All good :)".format(fpath), fg="green")


#############################################################################
# datademo collection
#############################################################################

@cli.group()
def collection():
    pass


@collection.command()  # NOQA
@collection_path_option
def summary(path):  # NOQA
    """Echo a json summary of the collection."""
    # The below will raise if the directory is not a collection.
    dtoolcore.Collection.from_path(path)

    num_datasets = 0
    num_files = 0
    tot_size = 0

    child_paths = [os.path.join(path, p) for p in os.listdir(path)]
    child_dirs = [d for d in child_paths if os.path.isdir(d)]

    for d in child_dirs:
        try:
            dataset = dtoolcore.DataSet.from_path(d)
        except (dtoolcore.DtoolTypeError, dtoolcore.NotDtoolObject):
            continue

        file_list = dataset.manifest["file_list"]
        size = sum([f["size"] for f in file_list])

        num_datasets += 1
        num_files += len(file_list)
        tot_size += size

    json_lines = [
        "{",
        '  "Number of datasets": {},'.format(num_datasets),
        '  "Number of files": {},'.format(num_files),
        '  "Total size": {}'.format(tot_size),
        "}",
    ]
    formatted_json = "\n".join(json_lines)
    colorful_json = pygments.highlight(
        formatted_json,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter())
    click.secho(colorful_json, nl=False)
