from os import environ
import unittest
from tests.test_brew_thermometer import TestBrewThermometer
from brew_thermometer.configuration import Configuration, DEFAULT_READ_INTERVAL_SECONDS, DEFAULT_LOOP_INTERVAL_SECONDS, BREW_THERMOMETER_DEV_FLAG
from brew_thermometer.logging import DEFAULT_LOG_LEVEL_STR


class TestConfiguration(TestBrewThermometer):
    def setUp(self):
        super()
        self.conf_hash = {
            'log_level': 'info',
            'read_interval_seconds': 20,
            'loop_interval_seconds': 1,
            'thermometers': [
                {
                    'id': 'foobarbaz',
                    'description': 'Foo bar baz',
                },
                {
                    'id': 'foobarbaz2',
                },
            ]
        }

    def test_is_developer_mode_detects_true(self):
        environ[BREW_THERMOMETER_DEV_FLAG] = '1'
        self.assertTrue(Configuration.is_developer_mode(),
                        msg="Configuration.is_developer_mode() should return true if the env variable "
                            "BREW_THERMOMETER_DEVELOPMENT is set to a truthy value")

    def test_is_developer_mode_detects_false(self):
        environ.pop(BREW_THERMOMETER_DEV_FLAG)
        self.assertFalse(Configuration.is_developer_mode(),
                         msg="Configuration.is_developer_mode() should return false if the env variable "
                             "BREW_THERMOMETER_DEVELOPMENT isnt' set or is set to a falsy value")

    def test_get_log_level(self):
        self.assertEqual(Configuration(self.conf_hash).get_log_level(), self.conf_hash['log_level'],
                         msg="get_log_level() should read the correct log level from the conf hash")

    def test_get_log_level_defaults(self):
        self.assertEqual(Configuration({}).get_log_level(), DEFAULT_LOG_LEVEL_STR,
                         msg="get_log_level() should return brew_thermometer.logging.DEFAULT_LOG_LEVEL_STR if a log "
                             "level isn't provided in the config hash")

    def test_get_read_interval_seconds(self):
        self.assertEqual(Configuration(self.conf_hash).get_read_interval_seconds(),
                         self.conf_hash['read_interval_seconds'],
                         msg="get_read_interval_seconds() should read the correct read_interval_seconds from the "
                             "conf hash")

    def test_get_read_interval_seconds_default(self):
        self.assertEqual(Configuration({}).get_read_interval_seconds(), DEFAULT_READ_INTERVAL_SECONDS,
                         msg="get_read_interval_seconds() should return "
                             "brew_thermometer.configuration.DEFAULT_READ_INTERVAL_SECONDS if read_interval_seconds "
                             "isn't specified in the conf hash")

    def test_get_loop_interval_seconds(self):
        self.assertEqual(Configuration(self.conf_hash).get_loop_interval_seconds(),
                         self.conf_hash['loop_interval_seconds'],
                         msg="get_loop_interval_seconds() should read the correct loop_interval_seconds from the "
                             "conf hash")

    def test_get_loop_interval_seconds_default(self):
        self.assertEqual(Configuration({}).get_loop_interval_seconds(), DEFAULT_LOOP_INTERVAL_SECONDS,
                         msg="get_loop_interval_seconds() should return "
                             "brew_thermometer.configuration.DEFAULT_LOOP_INTERVAL_SECONDS if loop_interval_seconds "
                             "isn't specified in the conf hash")

    def test_get_thermometer_configs_none_provided(self):
        self.assertEqual(Configuration({}).get_thermometer_configs(), [],
                         msg="If no thermometers are provided in the conf hash, get_thermometer_configs() should "
                             "return an empty list")

    def test_get_thermometer_configs_returns_correct_count(self):
        therm_conf_count = len(Configuration(self.conf_hash).get_thermometer_configs())
        self.assertEqual(therm_conf_count, len(self.conf_hash['thermometers']),
                         msg="get_thermometer_configs() should return one config for each thermometer in the conf hash")

    def test_get_thermometer_configs_returns_thermometers_with_specified_ids(self):
        specified_therm_ids = set([t['id'] for t in self.conf_hash['thermometers']])
        read_therm_ids = set([t.id for t in Configuration(self.conf_hash).get_thermometer_configs()])

        self.assertEqual(read_therm_ids, specified_therm_ids, msg="get_thermometer_configs() should read the correct "
                                                                  "id for each thermometer in the conf hash")

    def test_get_thermometer_configs_returns_thermometers_with_specified_descriptions(self):
        specified_descriptions = set()
        for thermometer in self.conf_hash['thermometers']:
            specified_descriptions.add(thermometer['description'] if 'description' in thermometer else '')

        read_descriptions = set(
            [t_conf.description for t_conf in Configuration(self.conf_hash).get_thermometer_configs()]
        )

        self.assertEqual(read_descriptions, specified_descriptions,
                         msg="get_thermometer_configs() should read the correct descriptino for each thermometer in "
                             "the conf hash or have an empty string if a description was not provided for the "
                             "thermometer")


if __name__ == '__main__':
    unittest.main()
