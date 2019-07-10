from unittest.mock import MagicMock, patch
import pytest


def pytest_configure(config):
    """Mock RPi.GPIO for all tests
    """
    # Given none of the tests can run without this being mocked, and
    # it's quite verbose, it's easiest to do it here with a pytest
    # hook (see
    # https://docs.pytest.org/en/2.7.3/plugins.html?highlight=re#well-specified-hooks)
    MockRPi = MagicMock()
    modules = {"RPi": MockRPi, "RPi.GPIO": MockRPi.GPIO}
    patcher = patch.dict("sys.modules", modules)

    patcher.start()
