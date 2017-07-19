"""datademo command line tool."""

import os
import json
import datetime

import yaml

import click
import dtoolcore
import pygments
import pygments.lexers
import pygments.formatters

from dtoolsid import __version__

dataset_path_option = click.argument(
    'dataset_path',
    type=click.Path(exists=True))

collection_path_option = click.argument(
    'collection_path',
    type=click.Path(exists=True))


@click.group()
@click.version_option(version=__version__)
def cli():
    """Command line utility to work with dtool datasets and collections."""


#############################################################################
# datademo dataset
#############################################################################

@cli.group()
def dataset():
    """Commands to work on a dataset."""


@dataset.command()
@dataset_path_option
def identifiers(dataset_path,):
    """Echo the identifiers in the dataset."""
    dataset = dtoolcore.DataSet.from_path(dataset_path)
    click.secho("\n".join(dataset.identifiers))


@dataset.command()
@dataset_path_option
def paths(dataset_path):
    """Echo the paths to the files in the dataset."""
    dataset = dtoolcore.DataSet.from_path(dataset_path)

    paths = [dataset.abspath_from_identifier(identifier)
             for identifier in dataset.identifiers]

    click.secho('\n'.join(paths))


@dataset.command()
@dataset_path_option
def manifest(dataset_path):
    """Echo the JSON manifest file."""
    dataset = dtoolcore.DataSet.from_path(dataset_path)
    formatted_json = json.dumps(dataset.manifest, indent=2)
    colorful_json = pygments.highlight(
        formatted_json,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter())
    click.secho(colorful_json, nl=False)


@dataset.command()
@dataset_path_option
def summary(dataset_path):
    """Echo a JSON summary of the dataset."""
    dataset = dtoolcore.DataSet.from_path(dataset_path)
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
@click.argument('new_dataset_path')
def template(dataset_path, new_dataset_path):
    """Create new empty dataset with metadata from existing dataset."""
    parent_dataset = dtoolcore.DataSet.from_path(dataset_path)

    output_dir, dataset_name = os.path.split(new_dataset_path)

    # There are ways of doing this that result in error messages where
    # the specific offending argument is highlighted.
    # http://click.pocoo.org/5/options/#callbacks-for-validation
    if os.path.exists(new_dataset_path):
        raise click.BadParameter(
            "Path already exists: {}".format(new_dataset_path)
        )
    if not os.path.isdir(output_dir):
        raise click.BadParameter(
            "Output directory does not exist: {}".format(output_dir)
        )

    # Create empty dataset
    new_dataset = dtoolcore.DataSet(dataset_name, data_directory="data")
    os.mkdir(new_dataset_path)
    new_dataset.persist_to_path(new_dataset_path)

    # Template the descriptive metadata.
    with open(parent_dataset.abs_readme_path) as fh:
        descriptive_metadata = yaml.load(fh)

    # Need explicit call to str() to ensure pyyaml does not mark up data with
    # Python types.
    descriptive_metadata["dataset_name"] = str(dataset_name)
    descriptive_metadata["creation_date"] = str(datetime.date.today())

    descriptive_metadata["parent_dataset"] = dict(path=parent_dataset._abs_path,
                                                  uuid=str(parent_dataset.uuid))

    with open(new_dataset.abs_readme_path, "w") as fh:
        yaml.dump(
            descriptive_metadata,
            fh,
            explicit_start=True,
            default_flow_style=False)


@dataset.command()
@dataset_path_option
def verify(dataset_path):
    """Verify the integrity of the dataset."""
    all_good = True
    dataset = dtoolcore.DataSet.from_path(dataset_path)
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

    abs_data_directory = os.path.join(dataset_path, dataset.data_directory)
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


@dataset.group()
def overlay():
    "Annotate the items in a dataset with an overlay."


@overlay.command()
@dataset_path_option
def illumina(dataset_path):
    """Create illumina metadata overlay for a dataset."""

    from dtoolsid.illumina import create_illumina_metadata_overlay
    dataset = dtoolcore.DataSet.from_path(dataset_path)

    create_illumina_metadata_overlay(dataset)

#############################################################################
# datademo collection
#############################################################################


@cli.group()
def collection():
    """Commands to work on a collection of datasets."""


@collection.command()  # NOQA
@collection_path_option
def summary(collection_path):  # NOQA
    """Echo a json summary of the collection."""
    # The below will raise if the directory is not a collection.
    dtoolcore.Collection.from_path(collection_path)

    num_datasets = 0
    num_files = 0
    tot_size = 0

    child_paths = [os.path.join(collection_path, p)
                   for p in os.listdir(collection_path)]
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
