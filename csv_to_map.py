import json

from utils.settings import Settings
from utils.mapping import Tile
from utils.mapping import csv_to_json

settings = Settings()


csv_to_json("map1", settings)