from os import path
import re


class Thermometer:
    """
    This class is used to read temperature from a DS18B20 thermometer
    """

    TEMP_LINE_REGEX = re.compile('t=(\d+)')

    def __init__(self, device_id, logger):
        self.device_id = device_id
        self._device_path = self._get_device_path(self.device_id)
        self._logger = logger.getChild("thermometer_{}".format(self.device_id))

    def get_temperature(self):
        """
        Attempts to read the temperature from the device, returns the temperature in 1/1000 degrees Celsius if
        temp was read, or None, otherwise.
        """
        read_data = self._read_device_data()
        if read_data:
            read_temp, temp = self._parse_temperature(self._read_device_data())
            if read_temp:
                return temp
            else:
                return None
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
    def _get_device_path(device_id):
        return path.join('/sys/bus/w1/devices', device_id, 'w1_slave')

    def _parse_temperature(self, data_str):
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
                        self._logger.error(
                            "Read temperature value '%s' could not be converted to an integer", m.group(1)
                        )
                        read_temp = False
                else:
                    self._logger.error(
                        "Could not parse temperature value from what was read from the thermometer device:\n%s\n",
                        read_temp
                    )
                    read_temp = False

            else:
                temp = None

            return read_temp, temp
        else:
            self._logger.error(
                "Data read from the thermometer device does not match expected format:\n%s\n",
                "\n".join(data_lines)
            )

            return False, None

    def _read_device_data(self):
        try:
            with open(self._device_path, 'r') as d:
                return d.read()
        except IOError as ioe:
            self._logger.error("Could not read data from '%s': %s", self._device_path, ioe)
            return None
