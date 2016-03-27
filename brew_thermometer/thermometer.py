from os import path
import re


class Thermometer:
    """
    This class is used to read temperature from a DS18B20 thermometer
    """

    TEMP_LINE_REGEX = re.compile('t=(\d+)')

    def __init__(self, device_id):
        self.device_id = device_id

    def get_temperature(self):
        """
        Attempts to read the temperature from the device, returns the temperature in 1/1000 degrees Celsius if
        temp was read, or None, otherwise.
        """
        read_temp, temp = self._parse_temperature(self._read_device_data())
        if read_temp:
            return temp
        else:
            return None

    def get_temperature_c(self):
        """
        Calls get_temperature and if a temp was read, returns that value converted to degrees Celsius, otherwise returns
        None.
        """
        temp = self.get_temperature()
        if temp:
            return float(temp) / 1000.0
        else:
            return None

    @staticmethod
    def _parse_temperature(data_str):
        """
        Returns a tuple, where the first value is a boolean denoting whether or not a temp was successfully read,
        and the second value is either:
          The temperature in 1/1000 degrees Celsius, if the first value is True
          - or -
          None, if the first value is not True
        """

        # output of the DS18B20 looks something like this:
        #   21 01 4b 46 7f ff 0c 10 1e : crc=1e YES
        #   21 01 4b 46 7f ff 0c 10 1e t=18062
        # where the ending 'YES' of the first line denotes that the temperature was successfully read
        # (will be 'NO' otherwise). The temperature is after the 't=' at the end of the second line. It is expressed in
        # 1/000 degrees Celsius
        data_lines = data_str.strip().splitlines()
        if len(data_lines) == 2:
            read_temp = data_lines[0].strip().endswith('YES')
            if read_temp:
                m = Thermometer.TEMP_LINE_REGEX.search(data_lines[1].strip())
                temp = None
                if m is not None:
                    try:
                        temp = int(m.group(1))
                    except ValueError:
                        # TODO: log error
                        read_temp = False
                else:
                    # TODO: log error
                    read_temp = False

            else:
                temp = None

            return read_temp, temp
        else:
            # TODO: log error
            return False, None

    def _read_device_data(self):
        # TODO: handle exceptions, log errors
        with open(path.join('/sys/bus/w1/devices', self.device_id, 'w1_slave')) as d:
            return d.read()
