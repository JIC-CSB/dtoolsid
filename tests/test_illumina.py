"""Test illumina module."""

from . import tmp_illumina_dataset


def test_tmp_dataset_fixture(tmp_illumina_dataset):

    assert len(tmp_illumina_dataset.identifiers) == 4


def test_parse_fastq_title_line():

    sample_title_line = \
        "@ST-E00317:319:HJMGJALXX:2:1101:7750:1309 1:N:0:NGTCACTA"

    from dtoolsid.illumina import parse_fastq_title_line

    result = parse_fastq_title_line(sample_title_line)

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
