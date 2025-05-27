import arcade
from constants import *

class Sword(arcade.Sprite):
    """ Class to represent the sword """
    def __init__(self):
        super().__init__(r"SpritesTempo/master_sword_down.png", SPRITE_SCALING)
        self.damage = 20  # Dégâts de l'épée