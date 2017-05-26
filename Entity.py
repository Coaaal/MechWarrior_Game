import pygame as pg
from settings import *

class Spritesheet:
    # loads and parses sprite sheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename)

    def get_image(self, x, y, width, height):
            image = pg.Surface((width, height))  # , pg.SRCALPHA, 32
            image.blit(self.spritesheet, (0, 0), (x, y, width, height))
            return image

class GameEntity(pg.sprite.Sprite):
    def __init__(self, world, width, height, asset_type=PLACEHOLDER):
        pg.sprite.Sprite.__init__(self)
        self.world = world
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.asset_type = asset_type
        self.image = self.world.sprite_sheet.get_image(self.asset_type[0],
                                                      self.asset_type[1],
                                                      self.asset_type[2],
                                                      self.asset_type[3])
        self.rect = self.image.get_rect()

    def spawn(self, x, y):
        # spawn entity at specified world coordinates
        pass