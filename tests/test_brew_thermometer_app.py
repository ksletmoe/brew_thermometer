import datetime
import unittest
from tests.test_brew_thermometer import TestBrewThermometer
from brew_thermometer.brew_thermometer_app import BrewThermometerApp


class TestBrewThermometerApp(TestBrewThermometer):
    def setUp(self):
        super()
        self.read_interval_seconds = 30
        self.app = BrewThermometerApp()
        self.app.read_interval_seconds = self.read_interval_seconds

    def test__should_read_thermometer_detects_it_should_read(self):
        # should read if last_read_time is None
        self.assertTrue(self.app._should_read_thermometer(None),
                        msg="_should_read_thermometer() should return True if last_read_time is None")

        # should read if the last_read_time is more than the read_interval_seconds value ago
        stale_last_read_time = datetime.datetime.now() - datetime.timedelta(seconds=self.read_interval_seconds + 10)
        self.assertTrue(self.app._should_read_thermometer(stale_last_read_time),
                        msg="_should_read_thermometer() should return True if last_read_time is more than "
                            "app.read_interval_seconds ago")

    def test__should_read_thermometer_detects_it_should_not_read(self):
        self.assertFalse(self.app._should_read_thermometer(datetime.datetime.now()))


if __name__ == '__main__':
    unittest.main()
