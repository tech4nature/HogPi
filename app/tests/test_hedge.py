from unittest.mock import patch
from unittest.mock import ANY

from shutil import copyfile

import hedge
import output

fileRW = output.Output()


@patch('hedge.thermo')
@patch('hedge.weight')
def test_run(mock_weight, mock_thermo):
    hedge.run('weight')
    writefile = 'weight.csv'
    avrgfile = 'avrgweight.csv'
    mock_weight.sensor().write.assert_called_with(writefile, debug=ANY, iterations=ANY)
    mock_weight.sensor().avrg.assert_called_with(writefile, avrgfile, ANY, ANY)

    hedge.run('temp')
    writefile = 'temp_out.csv'
    avrgfile = 'avrgtemp_out.csv'
    mock_thermo.sensor().write.assert_called()
    mock_thermo.sensor().avrg.assert_called_with(writefile, avrgfile, ANY)


@patch('hedge.client')
def test_post(mock_client):

    copyfile('/home/pi/app/tests/2000-01-01-00-00-01_int.mp4',
             '/home/pi/Videos/2000-01-01-00-00-01_int.mp4')
    data = [['2000 01 01 00 00 01', '20'], [
        '2000 01 01 00 00 01', '20'], ['2000 01 01 00 00 01', '20']]
    for i in data:
        fileRW.write('/home/pi/avrgweight.csv', i, True)
        fileRW.write('/home/pi/avrgtemp_in.csv', i, True)
        fileRW.write('/home/pi/avrgtemp_out.csv', i, True)
    hedge.post('box-9082242689124', 'hog-941_000021248873',
               {'weight': True, 'temp': True, 'video': True})
    mock_client.create_weight.assert_called()
    mock_client.create_inside_temp.assert_called()
    mock_client.create_outside_temp.assert_called()
    mock_client.upload_video.assert_called()
