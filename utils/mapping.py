import pygame
import json

class Tile(pygame.Rect):
    def __init__(self, *args):
        super().__init__(*args)


class GameMap():
    def __init__(self, settings, map_name):
        self.settings = settings
        self.map_name = map_name

        self.read_map()

    @property
    def map_location(self):
        return f"{self.settings.maps_location}{self.map_name}.json"

    def read_map(self):
        with open(self.map_location) as f:
            map_tiles = json.load(f)

        self.map_tiles = []
        for tile in map_tiles["tiles"]:
            if tile["tyle_type"] != "grass":
                tile["width"] = self.settings.cell_size
                tile["height"] = self.settings.cell_size
                self.map_tiles.append(self.create_tile(tile))

    def draw_map(self, screen):
        for tile in self.map_tiles:
            pygame.draw.rect(screen, tile.color, tile)

    @staticmethod
    def create_tile(tile_dict):
        tile = Tile(tile_dict["x"], tile_dict["y"], tile_dict["width"], tile_dict["height"])
        tile.tile_type = tile_dict["tyle_type"]
        if tile.tile_type == "wall":
            tile.color = pygame.Color("brown")
        elif tile.tile_type == "grass":
            tile.color = pygame.Color("grey")
        return tile



def csv_to_json(map_name, settings):
    input_file = f"{settings.maps_location}{map_name}.csv"
    output_file = f"{settings.maps_location}{map_name}.json"
    map_tiles = []
    with open(input_file) as f:
        for y_cell, line in enumerate(f):
            line = line.strip()
            for x_cell, tile in enumerate(line):
                if tile == "w":
                    map_tiles.append(
                        {"tyle_type": "wall", "x": settings.cell_size * x_cell, "y": settings.cell_size * y_cell})
                else:
                    map_tiles.append(
                        {"tyle_type": "grass", "x": settings.cell_size * x_cell, "y": settings.cell_size * y_cell})

    with open(output_file, "w") as f:
        json.dump({"tiles": map_tiles}, f)