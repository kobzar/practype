import logging


class CustomLogger:
    _instances = {}

    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    def __init__(self, loglevel="INFO", file=None, continue_write=False):
        if not hasattr(self, "_logger"):
            self._logger = logging.getLogger(str(id(self)))
            self._logger.setLevel(self.LOG_LEVELS.get(loglevel.upper(), logging.INFO))

            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

            if file:
                file_handler = logging.FileHandler(file, "a" if continue_write else "w")
                file_handler.setFormatter(formatter)
                self._logger.addHandler(file_handler)
            else:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                self._logger.addHandler(console_handler)

    def __getattr__(self, name):
        if name.startswith("_"):
            return object.__getattribute__(self, name)
        return getattr(self._logger, name)


# log = CustomLogger(loglevel="DEBUG", file="app.log", continue_write=False)
# log = CustomLogger(loglevel="DEBUG")
log = CustomLogger()

log.debug("Debug message")
log.warning("Warning message")

log.debug("_____Debug message")
log.warning("_____Warning message")
