import unittest
from unittest.mock import MagicMock
from brew_thermometer.thermometer import Thermometer


class TestThermometer(unittest.TestCase):
    def test__parse_temperature_temp_was_read(self):
        device_data = """21 01 4b 46 7f ff 0c 10 1e : crc=1e YES
                         21 01 4b 46 7f ff 0c 10 1e t=18062"""
        read_temp, _ = Thermometer._parse_temperature(device_data)
        self.assertTrue(read_temp, msg="First return tuple value should denote temperature was read")

    def test__parse_temperature_temp_was_not_read(self):
        device_data = """21 01 4b 46 7f ff 0c 10 1e : crc=1e NO
                         21 01 4b 46 7f ff 0c 10 1e t=18062"""
        read_temp, _ = Thermometer._parse_temperature(device_data)
        self.assertFalse(read_temp, msg="First return tuple response should denote temperature was not read")

    def test__parse_temperature_returns_none_for_garbage_input(self):
        device_data = "foo"
        read_temp, _ = Thermometer._parse_temperature(device_data)
        self.assertFalse(read_temp, msg="First return tuple value should be False if garbage is supplied for input")

    def test__parse_temperature_returns_correct_value(self):
        temp = 18062
        device_data = """21 01 4b 46 7f ff 0c 10 1e : crc=1e YES
                         21 01 4b 46 7f ff 0c 10 1e t={0}""".format(temp)
        _, read_temp = Thermometer._parse_temperature(device_data)
        self.assertEqual(read_temp, temp, msg="Second return tuple value should be the temperature data value")

    def test_get_temperature_returns_read_temperature_value(self):
        temp = 18062
        device_data = """21 01 4b 46 7f ff 0c 10 1e : crc=1e YES
                         21 01 4b 46 7f ff 0c 10 1e t={0}""".format(temp)
        t = Thermometer('28-021564dcdaff')
        t._read_device_data = MagicMock(return_value=device_data)
        self.assertEqual(t.get_temperature(), temp, msg="Should return the temperature if it was read")

    def test_get_temperature_returns_none_if_temp_was_not_read(self):
        device_data = """21 01 4b 46 7f ff 0c 10 1e : crc=1e NO
                         21 01 4b 46 7f ff 0c 10 1e t=18062"""
        t = Thermometer('28-021564dcdaff')
        t._read_device_data = MagicMock(return_value=device_data)
        self.assertEqual(t.get_temperature(), None, msg="Should return None if the temperature was not read")

    def test_get_temperature_c_returns_temp_in_c_if_read(self):
        temp = 18062
        device_data = """21 01 4b 46 7f ff 0c 10 1e : crc=1e YES
                         21 01 4b 46 7f ff 0c 10 1e t={0}""".format(temp)
        t = Thermometer('28-021564dcdaff')
        t._read_device_data = MagicMock(return_value=device_data)
        self.assertEqual(t.get_temperature_c(), float(temp) / 1000.0,
                         msg="Should return the temperature in degrees Celsius if it was read")

    def test_get_temperature_c_returns_none_if_temp_was_not_read(self):
        device_data = """21 01 4b 46 7f ff 0c 10 1e : crc=1e NO
                         21 01 4b 46 7f ff 0c 10 1e t=18062"""
        t = Thermometer('28-021564dcdaff')
        t._read_device_data = MagicMock(return_value=device_data)
        self.assertEqual(t.get_temperature_c(), None, msg="Should return None if the temperature was not read")


if __name__ == '__main__':
    unittest.main()
