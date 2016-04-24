from os import environ
import unittest
from unittest.mock import MagicMock
import brew_thermometer.configuration


class TestBrewThermometer(unittest.TestCase):
    """
    Base class for Brew Thermometer unittest classes that have code paths that would hit the filesystem for logging or
    reading config. Stubs out a few things to make tests work without hitting the filesystem.
    """
    def setUp(self):
        # set this to a truthy value so our logger doesn't attempt to log to a file during tests
        environ[brew_thermometer.configuration.BREW_THERMOMETER_DEV_FLAG] = 1

        # mock reading the config file
        brew_thermometer.configuration.load_config = MagicMock(
            return_value={
                "log_level": "info",
                "read_interval_seconds": 30,
                "loop_interval_seconds": 1,
                "thermometers": []
            }
        )
