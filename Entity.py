import pygame as pg
from settings import *
vec = pg.math.Vector2

class Spritesheet:
    # loads and parses sprite sheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
            image = pg.Surface((width, height))
            image.blit(self.spritesheet, (0,0), (x,y,width,height))
            return image

class GameEntity(pg.sprite.Sprite):
    def __init__(self, game, width, height, asset_type=PLACEHOLDER):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.asset_type = asset_type
        self.image = PLACEHOLDER
        if self.asset_type == PLACEHOLDER:
            self.image = self.game.sprite_sheet.get_image(PLACEHOLDER[0],
                                                          PLACEHOLDER[1],
                                                          PLACEHOLDER[2],
                                                          PLACEHOLDER[3])
        elif self.asset_type == DESSERT:
            self.image = self.game.sprite_sheet.get_image(DESSERT[0],
                                                          DESSERT[1],
                                                          DESSERT[2],
                                                          DESSERT[3])
        self.rect = self.image.get_rect()

    def spawn(self, x, y):
        # spawn entity at specified world coordinates
        pass

    def update(self):
        pass