import unittest
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


if __name__ == '__main__':
    unittest.main()
