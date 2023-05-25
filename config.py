from configparser import ConfigParser
from dataclasses import asdict, dataclass, fields, is_dataclass
from typing import List


@dataclass
class Employe:
    name: str = ""
    age: int = 0
    position: str = ""


@dataclass
class Book:
    name: str = "Mooglee"


data_classes = [Book, Employe]


class Cfg:
    def __init__(self, data_classes, file_path):
        self.data_classes = data_classes
        self.file_path = file_path
        self.config = ConfigParser()
        self.loaded_data = {}

    def save_to_ini(self):
        # config = ConfigParser()

        for cls in self.data_classes:
            section = cls.__name__

            if section in self.loaded_data:
                instance = self.loaded_data[section]
            else:
                instance = cls()

            obj_dict = asdict(instance)
            self.config[section] = {field: str(value) for field, value in obj_dict.items()}

        with open(self.file_path, "w") as config_file:
            self.config.write(config_file)

    def load_from_ini(self):
        # config = ConfigParser()
        # self.loaded_data = {}

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
                    obj_dict[field_name] = field.type(value)

            obj = cls(**obj_dict)
            self.loaded_data[section] = obj

    def __getattr__(self, name):
        if name in self.loaded_data:
            return self.loaded_data[name]
        else:
            raise AttributeError(f"'Cfg' object has no attribute '{name}'")


cfg = Cfg(data_classes, "config.ini")
cfg.load_from_ini()

# print(cfg.Book.name)
# cfg.Book.name = "Cruzo1"
# print(cfg.Book.name)

cfg.save_to_ini()
