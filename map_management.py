import arcade
from constants import *

class Map:
    def __init__(self, filenames, layer_options, collisions):

        # Map informations
        self.filenames = filenames
        self.layer_options = layer_options
        self.collisions = collisions
        self.current_map = 0

    def load_map(self, map_index = 0):

        # Define the current map
        self.current_map = map_index

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(self.filenames[self.current_map],
                                            TILE_SCALING,
                                            self.layer_options[self.current_map])
        self.end_left = 0
        self.end_bottom = 0
        self.end_right = self.tile_map.width * (28 * TILE_SCALING)
        self.end_top = self.tile_map.height * (28 * TILE_SCALING)
        
        self.scene = arcade.Scene.from_tilemap(self.tile_map)