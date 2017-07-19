"""Test illumina module."""

from . import tmp_illumina_dataset  # NOQA


def test_tmp_dataset_fixture(tmp_illumina_dataset):  # NOQA

    assert len(tmp_illumina_dataset.identifiers) == 4


def check_fastq_read_1_sample_result(result):

    assert result["instrument"] == "ST-E00317"
    assert result["run_number"] == 319
    assert result["flowcell_id"] == "HJMGJALXX"
    assert result["lane"] == 2
    assert result["tile"] == 1101
    assert result["x_pos"] == 7750
    assert result["y_pos"] == 1309
    assert result["read"] == 1
    assert result["is_filtered"] is False
    assert result["control_number"] == 0
    assert result["index_sequence"] == "NGTCACTA"


def test_parse_fastq_title_line():

    sample_title_line = \
        "@ST-E00317:319:HJMGJALXX:2:1101:7750:1309 1:N:0:NGTCACTA"

    from dtoolsid.illumina import parse_fastq_title_line

    result = parse_fastq_title_line(sample_title_line)

    check_fastq_read_1_sample_result(result)


def test_parse_fastq_title_line_sample_num_edge_case():

    from dtoolsid.illumina import parse_fastq_title_line

    sample_title_line = \
        "@ST-E00317:319:HJMGJALXX:2:1101:7750:1309 1:N:0:NGTCACTA"
    result = parse_fastq_title_line(sample_title_line)
    assert result["index_sequence"] == "NGTCACTA"

    sample_title_line = \
        "@ST-E00317:319:HJMGJALXX:2:1101:7750:1309 1:N:0:2"
    result = parse_fastq_title_line(sample_title_line)
    assert result["index_sequence"] == "2"


def test_extract_metadata_from_fastq_file_object(tmp_illumina_dataset):  # NOQA

    from dtoolsid.illumina import extract_metadata_from_fastq_file_object

    fastq_file_identifier = "42889f278935f206dcf2772c81a055b338844c48"
    fastq_filename = tmp_illumina_dataset.abspath_from_identifier(
        fastq_file_identifier
    )

    with open(fastq_filename) as fh:
        result = extract_metadata_from_fastq_file_object(fh)

    check_fastq_read_1_sample_result(result)


def test_extract_metadata_from_fastq_file(tmp_illumina_dataset):  # NOQA

    from dtoolsid.illumina import extract_metadata_from_fastq_file

    # Test plaintext fastq file
    fastq_file_identifier = "42889f278935f206dcf2772c81a055b338844c48"
    fastq_filename = tmp_illumina_dataset.abspath_from_identifier(
        fastq_file_identifier
    )

    result = extract_metadata_from_fastq_file(fastq_filename)

    check_fastq_read_1_sample_result(result)

    # Test a gzipped fastq file
    fastq_gz_file_identifier = "40ed0c9553797c66cfa07cefb37af9086a5da66b"
    fastq_gz_filename = tmp_illumina_dataset.abspath_from_identifier(
        fastq_gz_file_identifier
    )

    result = extract_metadata_from_fastq_file(fastq_gz_filename)

    check_fastq_read_1_sample_result(result)


def test_create_illumina_metadata_overlay(tmp_illumina_dataset):  # NOQA

    from dtoolsid.illumina import create_illumina_metadata_overlay

    create_illumina_metadata_overlay(tmp_illumina_dataset)

    overlays = tmp_illumina_dataset.access_overlays()

    assert "illumina_metadata" in overlays

    first_identifier = "42889f278935f206dcf2772c81a055b338844c48"
    first_metadata = overlays["illumina_metadata"][first_identifier]
    check_fastq_read_1_sample_result(first_metadata)

    first_gz_identifier = "40ed0c9553797c66cfa07cefb37af9086a5da66b"
    first_gz_metadata = overlays["illumina_metadata"][first_gz_identifier]
    check_fastq_read_1_sample_result(first_gz_metadata)

