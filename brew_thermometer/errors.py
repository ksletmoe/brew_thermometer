class BrewThermometerAppError(Exception):
    pass


class ConfigurationError(BrewThermometerAppError):
    pass


class ReporterError(BrewThermometerAppError):
    pass
