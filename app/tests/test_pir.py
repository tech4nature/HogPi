from unittest.mock import patch
from unittest.mock import ANY

import pir


@patch('pir.RPi')
def test_setup_and_read(mock_rpi):
    """Check the pin is set up correctly, and read.

    This test isn't very useful as it just checks arguments are passed
    to GPIO subsystem correctly.

    """
    pin_number = 1
    test_sensor = pir.sensor(pin_number)
    mock_rpi.GPIO.setmode.assert_called()
    mock_rpi.GPIO.setup.assert_called_with(pin_number, ANY, pull_up_down=ANY)

    test_sensor.read()
    mock_rpi.GPIO.input.assert_called_with(pin_number)
