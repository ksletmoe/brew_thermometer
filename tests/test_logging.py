import unittest
import logging
from brew_thermometer.logging import _get_log_level


class TestLogging(unittest.TestCase):
    def test__get_log_level_debug(self):
        self.assertEqual(_get_log_level('debug'), logging.DEBUG,
                         msg="_get_log_level() should return logging.DEBUG if provided 'debug'")

    def test__get_log_level_info(self):
        self.assertEqual(_get_log_level('info'), logging.INFO,
                         msg="_get_log_level() should return logging.INFO if provided 'info'")

    def test__get_log_level_warning(self):
        self.assertEqual(_get_log_level('warning'), logging.WARNING,
                         msg="_get_log_level() should return logging.WARNING if provided 'warning'")

    def test__get_log_level_error(self):
        self.assertEqual(_get_log_level('error'), logging.ERROR,
                         msg="_get_log_level() should return logging.ERROR if provided 'error'")

    def test__get_log_level_critical(self):
        self.assertEqual(_get_log_level('critical'), logging.CRITICAL,
                         msg="_get_log_level() should return logging.CRITICAL if provided 'critical'")

if __name__ == '__main__':
    unittest.main()
