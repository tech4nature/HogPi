import sftp
from unittest.mock import ANY
from unittest.mock import patch


@patch("sftp.pysftp")
@patch("sftp.os")
def test_with_mp4(mock_os, mock_pysftp):
    mock_pysftp.Connection().listdir.return_value = ["test.mp4", "test1.mp4"]
    sftp.pull_videos("8.8.8.8", "john", "password")
    mock_pysftp.Connection.assert_called()
    mock_pysftp.Connection().chdir.assert_called()
    mock_pysftp.Connection().get.assert_called()


@patch("sftp.pysftp")
@patch("sftp.os")
def test_without_mp4(mock_os, mock_pysftp):
    mock_pysftp.Connection().listdir.return_value = ["test.mp3", "test1.mov"]
    sftp.pull_videos("8.8.8.8", "john", "password")
    mock_pysftp.Connection.assert_called()
    mock_pysftp.Connection().chdir.assert_called()
    mock_pysftp.Connection().get.assert_not_called()
