import sftp

from unittest.mock import ANY
from unittest.mock import patch


@patch('sftp.pysftp')
def test_with_mp4(mock_pysftp):
    sftp.pull_videos('8.8.8.8', 'john', 'password')
    mock_pysftp.Connection.assert_called()
    mock_pysftp.Connection.cd.assert_called()
    mock_pysftp.Connection.list_dir.return_value = ['test.mp4', 'test1.mp4']
    assertEqual(mock_pysftp.Connection.get.call_count, 2)


@patch('sftp.pysftp')
def test_without_mp4(mock_pysftp):
    sftp.pull_videos('8.8.8.8', 'john', 'password')
    mock_pysftp.Connection.assert_called()
    mock_pysftp.Connection.cd.assert_called()
    mock_pysftp.Connection.list_dir.return_value = ['test.mp3', 'test1.mov']
    assertEqual(mock_pysftp.Connection.get.call_count, 0)