from unittest.mock import MagicMock, patch

MockRPi = MagicMock()
modules = {
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO,
}
patcher = patch.dict("sys.modules", modules)
patcher.start()

@patch('rfid.serial')
def test_main(mock_serial):
    from hedge import main
    main()
