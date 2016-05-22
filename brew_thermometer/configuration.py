import json
from os import environ

from brew_thermometer.errors import ConfigurationError
from brew_thermometer.logging import get_logger, DEFAULT_LOG_LEVEL_STR


BREW_THERMOMETER_DEV_FLAG = 'BREW_THERMOMETER_DEVELOPMENT'
BREW_THERMOMETER_CONFIG_ENV_VAR = 'BREW_THERMOMETER_CONFIG'
DEFAULT_CONFIG_PATH = '/etc/brew_thermometer/config.json'
DEFAULT_READ_INTERVAL_SECONDS = 30
DEFAULT_LOOP_INTERVAL_SECONDS = 1


class Configuration:
    def __init__(self, config_hash):
        self._config_hash = config_hash
        self._logger = get_logger(self.get_log_level(), __name__, self.is_developer_mode())

    def get_log_level(self):
        if 'log_level' in self._config_hash:
            return self._config_hash['log_level']
        else:
            return DEFAULT_LOG_LEVEL_STR

    @staticmethod
    def is_developer_mode():
        if BREW_THERMOMETER_DEV_FLAG in environ and environ[BREW_THERMOMETER_DEV_FLAG]:
            return True
        else:
            return False

    def get_read_interval_seconds(self):
        return self._parse_int('read_interval_seconds', DEFAULT_READ_INTERVAL_SECONDS)

    def get_loop_interval_seconds(self):
        return self._parse_int('loop_interval_seconds', DEFAULT_LOOP_INTERVAL_SECONDS)

    def get_thermometer_configs(self):
        return self._parse_thermometer_configs()

    def get_temperature_reporter_config(self):
        return self._config_hash['aws_iot_configuration']

    def _parse_int(self, conf_key, default_val):
        if conf_key in self._config_hash:
            conf_val = self._config_hash[conf_key]
            try:
                return int(conf_val)
            except ValueError:
                self._logger.warning(
                    "Invalid value for '{}': {}; the value must be an integer. Defaulting to {}",
                    conf_key,
                    conf_val,
                    default_val
                )

        return default_val

    def _parse_thermometer_configs(self):
        therm_configs = []

        if 'thermometers' in self._config_hash:
            for therm_conf in self._config_hash['thermometers']:
                if 'id' in therm_conf and therm_conf['id']:
                    description = therm_conf['description'] if 'description' in therm_conf else ""
                    therm_configs.append(ThermometerConfiguration(therm_conf['id'], description))

        return therm_configs


class ThermometerConfiguration:
    def __init__(self, id, description):
        self.id = id
        self.description = description


def load_config():
    """
    Valid config as follows:
    {
        "log_level": "warning",  # valid values: debug, info, warning, error, critical
        "read_interval_seconds": 30,  # how often to read and report values. if not specified, defaults to DEFAULT_READ_INTERVAL_SECONDS
        "loop_interval_seconds": 1,  # how often to check to see if we need to read each thermometer. if not specified, defaults to DEFAULT_loop_INTERVAL_SECONDS
        thermometers: [
            {
                "id": "28-0000075eddab",  # the device ID of the thermometer
                "description": "Fermenter (Internal)"  # human readable description of the thermometer (e.g. "ambient air", "fermenter", etc.)
            },
            ...
        ],
        "aws_iot_configuration": {
            "host": "",
            "port": 8883,
            "certificate_authority_cert_file_path": "",
            "cert_file_path": "",
            "private_key_path": "",
            "thing_name": "BrewThermometer",
            "topic_name": "temperature"
        }
    }
    """
    conf_path = get_config_file_path()
    try:
        with open(conf_path, 'r') as conf_file:
            conf = json.load(conf_file)
    except OSError as e:
        raise ConfigurationError("Cannot open configuration file {}: {}".format(conf_path, e))
    except json.JSONDecodeError as e:
        raise("Cannot open configuration file {}: {}".format(conf_path, e))

    return Configuration(conf)


def get_config_file_path():
    if BREW_THERMOMETER_CONFIG_ENV_VAR in environ:
        return environ[BREW_THERMOMETER_CONFIG_ENV_VAR]
    else:
        return DEFAULT_CONFIG_PATH
