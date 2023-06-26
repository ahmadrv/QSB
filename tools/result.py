from pathlib import Path
import os

# [ ]: Make this module more efficient!!!


def make_csv_with_header(file_path, header):
    """
    This method makes a csv file with header.
    """

    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)
        with open(file_path, "w") as f:
            f.write(header + "\n")


def add_result_to_file(result, file_path):
    """
    This method adds the result to the file.
    """

    with open(file_path, "a") as f:
        f.write(result + "\n")
