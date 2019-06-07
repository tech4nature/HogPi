import os
from unittest.mock import patch
from unittest.mock import ANY
import tempfile

from output import Output


def test_read_write():
    """Can we round-trip a data array to and from the filesystem?
    """
    filename = tempfile.NamedTemporaryFile().name
    test_output = Output()
    # XXX what happens if different length rows are written?
    # XXX also what if numeric rather than strings?
    test_data = [['1', '2', '3'], ['4', '5', '6']]
    for row in test_data:
        test_output.write(filename, row)

    for i in range(len(test_data[0])):
        return_val = test_output.read(filename, i)
        expected = [x[i] for x in test_data]
        assert return_val == expected


def test_clear_data():
    """Does clearing data result in an empty file?
    """
    filename = tempfile.NamedTemporaryFile().name
    with open(filename, "w") as f:
        f.write(" ")
    assert os.path.exists(filename)

    test_output = Output()
    test_output.clear_data(filename)
    with open(filename, "r") as f:
        assert not f.read()
