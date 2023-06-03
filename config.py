import logging
import os
from configparser import ConfigParser
from dataclasses import asdict, dataclass, fields

a = 10
if a == 0:
    pass
elif a >= 5:
    pass


class LogConf:
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


class Cfg:
    """Main config App"""

    # Use Singleton method for this class
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    # Init class
    def __init__(self, data_classes, file_path):
        if not hasattr(self, "initialized"):
            self.data_classes = data_classes
            self.file_path = file_path
            self.config = ConfigParser()
            self.loaded_data = {}
            self.initialized = True
            self.__load()

    # Save configuration in file
    def save(self):
        for cls in self.data_classes:
            section = cls.__name__

            if not self.config.has_section(section):
                self.config.add_section(section)

            if section in self.loaded_data:
                instance = self.loaded_data[section]
            else:
                instance = cls()

            obj_dict = asdict(instance)
            for field, value in obj_dict.items():
                if isinstance(value, bool):
                    self.config.set(section, field, str(value).lower())
                else:
                    self.config.set(section, field, str(value))

        with open(self.file_path, "w") as config_file:
            self.config.write(config_file)

    # Load data
    def __load(self):
        try:
            self.config.read(self.file_path)
        except Exception as e:
            print(f"Error reading INI file: {e}")
            print("Loading default values instead.")
            self.loaded_data = {cls.__name__: cls() for cls in self.data_classes}
            return

        for cls in self.data_classes:
            section = cls.__name__

            if not self.config.has_section(section):
                print(f"Section {section} not found in INI file. Loading default values.")
                self.loaded_data[section] = cls()
                continue

            obj_dict = {}

            for field in fields(cls):
                field_name = field.name
                if self.config.has_option(section, field_name):
                    value = self.config.get(section, field_name)
                    if field.type is bool:
                        value = value.lower() in ["true", "yes", "1"]
                    elif field.type is int:
                        value = int(value)
                    elif field.type is float:
                        value = float(value)
                    obj_dict[field_name] = value

            obj = cls(**obj_dict)
            self.loaded_data[section] = obj

    def __getattr__(self, name):
        if name == "loaded_data":
            raise AttributeError(f"'Cfg' object has no attribute '{name}'")

        if name in self.loaded_data:
            return self.loaded_data[name]
        else:
            raise AttributeError(f"'Cfg' object has no attribute '{name}'")


@dataclass
class App:
    name: str = ""


@dataclass
class Log:
    fresh: bool = True
    logfile: str = "practype.log"
    level: str = "DEBUG"


# Init configuration
configurations = [App, Log]
cfg = Cfg(configurations, "config.ini")

# Init logger
log = LogConf(loglevel=cfg.Log.level, file=cfg.Log.logfile, continue_write=cfg.Log.fresh)

if __name__ == "__main__":
    pass
