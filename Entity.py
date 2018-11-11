import pygame as pg
import time
from settings import TILE_SIZE


class SpriteSheet:
    # loads and parses sprite sheets
    def __init__(self, filename):
        self.sprite_sheet = pg.image.load(filename)

    def get_image(self, x, y, width, height):
            my_image = pg.Surface((width, height), pg.SRCALPHA)  # , pg.SRCALPHA, 32
            my_image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
            return my_image

    # def get_rect(self):


class GameEntity(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        super(GameEntity, self).__init__()
        # pg.sprite.Sprite.__init__(self)
        self.world = kwargs.get('world')
        self.name = kwargs.get('name')
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.x = 0
        self.y = 0
        self.asset_type = kwargs.get('asset_type')
        self.image = self.world.sprite_sheet.get_image(self.asset_type[0],
                                                       self.asset_type[1],
                                                       self.asset_type[2],
                                                       self.asset_type[3])
        self.rect = self.image.get_rect()
        self.spawn_time = time.time()

    def spawn(self, x, y):
        # spawn entity at specified world coordinates
        pass

