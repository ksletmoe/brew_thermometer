import logging
from logging.handlers import TimedRotatingFileHandler
from brew_thermometer.errors import ConfigurationError


LOG_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
DEFAULT_LOG_LEVEL_STR = 'warning'
PRODUCTION_LOG_FILE = '/var/log/brew_thermometer/brew_thermometer.log'


def get_logger(config_log_level, logger_name, developer_mode=False):
    conf_error = None

    logger = logging.getLogger(logger_name)
    if developer_mode:
        from logging import StreamHandler
        log_handler = StreamHandler()
        log_handler.setLevel(logging.DEBUG)
    else:
        log_handler = TimedRotatingFileHandler(PRODUCTION_LOG_FILE, when='midnight', interval=1, backupCount=7)
        try:
            log_level = _get_log_level(config_log_level)
        except ConfigurationError as ce:
            conf_error = ce
            log_level = _get_log_level(DEFAULT_LOG_LEVEL_STR)
        log_handler.setLevel(log_level)

    log_handler.setFormatter(LOG_FORMATTER)
    logger.addHandler(log_handler)

    if conf_error:
        logger.warning("Error getting log level from configuration: {}".format(conf_error))

    return logger


def _get_log_level(config_log_level):
    if config_log_level.lower() == 'debug':
        return logging.DEBUG
    elif config_log_level.lower() == 'info':
        return logging.INFO
    elif config_log_level.lower() == 'warning':
        return logging.WARNING
    elif config_log_level.lower() == 'error':
        return logging.ERROR
    elif config_log_level.lower() == 'critical':
        return logging.CRITICAL
    else:
        raise ConfigurationError(
            "Invalid log level '{}' supplied; must be one of: debug, info, warning, error, or critical".format(
                config_log_level)
        )
