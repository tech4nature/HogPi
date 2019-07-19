import pytest
import datetime
import os
import io
import tempfile

from unittest.mock import ANY
from unittest.mock import patch


from thermo import sensor


@patch("thermo.os")
@patch("thermo.glob")
def test_setup(mock_glob, mock_os):
    """Is thermostat set up with modprobe?
    """
    # All the other stuff is setup and most of it unecessary globals.
    # We don't bother testing the actual calls; these should really
    # live outside the code anyway.
    mock_glob.glob.return_value = ['hi']
    sensor()
    mock_os.system.assert_called()


@patch("thermo.os")
@patch("thermo.glob")
@patch("thermo.datetime")
def test_read(mock_datetime, mock_glob, mock_os):
    # https://www.kernel.org/doc/Documentation/w1/slaves/w1_therm:
    # The first line contains the nine hex bytes read along with a
    # calculated crc value and YES or NO if it matched.
    # If the crc matched the returned values are retained.  The second line
    # displays the retained values along with a temperature in millidegrees
    # Centigrade after t=.
    w1_data = [
        "a3 01 4b 46 7f ff 0e 10 d8 : crc=d8 YES\n",
        "a3 01 4b 46 7f ff 0e 10 d8 t=32768\n",
    ]
    w2_data = [
        "a3 01 4b 46 7f ff 0e 10 d8 : crc=d8 YES\n",
        "a3 01 4b 46 7f ff 0e 10 d8 t=22768\n",
    ]
    dummy_time = datetime.datetime(2000, 1, 1)
    mock_datetime.now.return_value = dummy_time
    # Set up files with mock content to replicate w1_therm devices
    with tempfile.TemporaryDirectory() as device_1, tempfile.TemporaryDirectory() as device_2:
        sensor_1_name = os.path.join(device_1, "w1_slave")
        sensor_2_name = os.path.join(device_2, "w1_slave")
        with open(sensor_1_name, "w") as f:
            f.writelines(w1_data)
        with open(sensor_2_name, "w") as f:
            f.writelines(w2_data)
        mock_glob.glob.return_value = [device_1, device_2]

        temp_sensor = sensor()
        result = temp_sensor.read()
    # Note that the order is reversed because they are returned in the
    # order of the `temp_sensors` list
    assert result == [
        ("2000 01 01 00 00 00", sensor_1_name, 32.768),
        ("2000 01 01 00 00 00", sensor_2_name, 22.768),
    ]


@pytest.mark.xfail
def test_write():
    """Does this read from sensors and write the result to file?
    """
    raise BaseException("Test not implemented")


@pytest.mark.xfail
def test_avrg():
    raise BaseException("Test not implemented")
