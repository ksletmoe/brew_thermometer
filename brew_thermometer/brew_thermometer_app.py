import datetime
from time import sleep
from brew_thermometer.thermometer import Thermometer
from brew_thermometer.configuration import load_config
from brew_thermometer.logging import get_logger


class BrewThermometerApp:
    def __init__(self):
        config = load_config()
        self._logger = get_logger(config.get_log_level(), __name__, config.is_developer_mode())
        self._thermometers = self._load_thermometers(config.get_thermometer_configs())
        self.read_interval_seconds = config.get_read_interval_seconds()
        self.loop_interval_seconds = config.get_loop_interval_seconds()

    def run(self):
        while True:
            try:
                self._logger.debug("Looping")
                read_temp_ids = self._try_read_thermometers()
                reported_temp_ids = self._report_read_temperatures(read_temp_ids)
                self._record_reported_temps(reported_temp_ids)
            except Exception as e:
                self._logger.error("Error while reading thermometers: {}".format(e))

            sleep(self.loop_interval_seconds)

    def _try_read_thermometers(self):
        # TODO
        return []

    def _should_read_thermometer(self, last_read_time):
        if last_read_time is None or \
                        (datetime.datetime.now() - last_read_time).total_seconds() > self.read_interval_seconds:
            return True
        else:
            return False

    def _report_read_temperatures(self, read_temp_ids):
        # TODO
        return []

    def _record_reported_temps(self, reported_temp_ids):
        # TODO
        pass

    def _load_thermometers(self, thermometer_configs):
        thermometers = {}

        for conf in thermometer_configs:
            thermometers[conf.id] = {
                'thermometer': Thermometer(conf.id, self._logger),
                'description': conf.description,
                'last_read': None
            }

        return thermometers
