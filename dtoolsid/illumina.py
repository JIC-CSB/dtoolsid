"""Module for working with Illumina FASTQ files."""


def parse_fastq_title_line(fastq_title_line):

    def illumina_bool(x):
        if x == "Y":
            return True
        if x == "N":
            return False
        raise(ValueError)

    component_names = [
        ("instrument", str),
        ("run_number", int),
        ("flowcell_id", str),
        ("lane", int),
        ("tile", int),
        ("x_pos", int),
        ("y_pos", int),
        ("read", int),
        ("is_filtered", illumina_bool),
        ("control_number", int),
        ("index_sequence", str)
    ]

    assert fastq_title_line[0] == '@'

    words = fastq_title_line[1:].split(" ")

    assert len(words) == 2

    components = words[0].split(":") + words[1].split(":")

    assert len(components) == len(component_names)

    # We were going through a functional phase
    return {
        name: cast_func(component)
        for (name, cast_func), component
        in zip(component_names, components)
    }
