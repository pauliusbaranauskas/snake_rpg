import os
import json

class Settings():
    """Class to read, update, save settings.
    Takes everything from snake settings.json file and uses as attributes.
    """
    cell_number: int
    cell_size: int
    framerate: int

    def __init__(self):
        self.get_file_path()
        self.read_settings()

    def get_file_path(self):
        """Gets path to settings file.
        """
        file_path = os.path.realpath(__file__)
        sep = os.path.sep
        file_path = file_path.split(sep)
        file_path = file_path[:-2]
        assets_location = file_path.copy()
        assets_location.extend(["assets", ""])
        self.assets_location = sep.join(assets_location)
        file_path.append("snake settings.json")
        self.file_path = sep.join(file_path)

    def read_settings(self):
        """Reads settings from settings json.
        By default, this file is located in game directory as "snake settings.json" file.
        """
        with open(self.file_path) as f:
            settings = f.read()
            self.settings = json.loads(settings)
        for key, value in self.settings.items():
            setattr(self, key, value)

    def save_settings(self):
        """Saves settings to settings json file.
        By default, this file is located in game directory as "snake settings.json" file.
        """
        with open(self.file_path, 'w') as f:
            json.dump(self.settings, f)

    def update(self, attr, value):
        """Updates (or creates new) setting.

        Args:
            attr (str): Settings option/attribute.
            value (any): Any value to add/update.
        """
        self.settings[attr] = value
        setattr(self, attr, value)

    def update_numeric(self, attr, value):
        """Updates (or creates new) setting integer value. If provided value is not numeric, then saves 0.

        Args:
            attr (str): attribute/setting name.
            value (int): Integer value to add to settings.
        """
        try:
            value = int(value)
        except ValueError:
            value = 0
        self.update(attr, value)

    @property
    def height(self):
        """Vertical size of game area in pixels.

        Returns:
            int: Vertical size of game area in pixels.
        """
        return self.cell_number * self.cell_size

    @property
    def width(self):
        """Horizontal size of game area in pixels.

        Returns:
            int: Horizontal size of game area in pixels.
        """
        return self.cell_number * self.cell_size

    def revert(self):
        """Resets settings to last saved value.
        """
        self.__init__()

    def __str__(self):
        return self.settings.__str__()
