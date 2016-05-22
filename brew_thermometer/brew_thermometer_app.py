import datetime
import traceback
from time import sleep
from brew_thermometer.thermometer import Thermometer
from brew_thermometer.configuration import load_config
from brew_thermometer.logging import get_logger
from brew_thermometer.aws_iot_reporter import AwsIotReporter


class BrewThermometerApp:
    def __init__(self):
        config = load_config()
        self._logger = get_logger(config.get_log_level(), __name__, config.is_developer_mode())
        self._thermometers = self._load_thermometers(config.get_thermometer_configs())
        self._temperature_reporter = AwsIotReporter(config.get_temperature_reporter_config(), self._logger)
        self.read_interval_seconds = config.get_read_interval_seconds()
        self.loop_interval_seconds = config.get_loop_interval_seconds()

    def run(self):
        while True:
            try:
                self._logger.debug("Looping")
                read_temps = self._try_read_thermometers()
                reported_temp_ids = self._report_read_temperatures(read_temps)
                self._record_reported_temps(reported_temp_ids)
            except Exception as e:
                self._logger.error("Error while reading thermometers: {}\n\n".format(e, ))
                self._logger.exception(traceback.format_exc())

            sleep(self.loop_interval_seconds)

    def _try_read_thermometers(self):
        read_values = {}
        for thermometer_id, thermometer_info in iter(self._thermometers.items()):
            if self._should_read_thermometer(thermometer_info["last_read"]):
                temp = thermometer_info['thermometer'].get_temperature_c()
                if temp is not None:
                    self._logger.debug("Read temperature %s from thermometer %s", str(temp), thermometer_id)
                    read_values[thermometer_id] = temp
                else:
                    self._logger.warn("Could not read thermometer with ID {0}".format(thermometer_id))

        return read_values

    def _should_read_thermometer(self, last_read_time):
        if last_read_time is None or \
                (datetime.datetime.now() - last_read_time).total_seconds() > self.read_interval_seconds:
            return True
        else:
            return False

    def _report_read_temperatures(self, read_temps):
        successful_reports = []
        for thermometer_id, temp_degrees_c in iter(read_temps.items()):
            payload = {
                "thermometer_id": thermometer_id,
                "description": self._thermometers[thermometer_id]["description"],
                "temperature_degrees_celsius": temp_degrees_c
            }

            if self._temperature_reporter.publish_payload(payload):
                self._logger.debug("Published payload: %s", str(payload))
                successful_reports.append(thermometer_id)

        return successful_reports

    def _record_reported_temps(self, reported_temp_ids):
        for thermometer_id in reported_temp_ids:
            self._thermometers[thermometer_id]["last_read"] = datetime.datetime.now()

    def _load_thermometers(self, thermometer_configs):
        thermometers = {}

        for conf in thermometer_configs:
            self._logger.debug("Thermometer: %s - %s", conf.id, conf.description)
            thermometers[conf.id] = {
                'thermometer': Thermometer(conf.id, self._logger),
                'description': conf.description,
                'last_read': None
            }

        return thermometers
