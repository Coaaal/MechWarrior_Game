#sprite classes for platformer
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


# the player directly affects the camera, but the player is always centered in the camera
class Player(GameEntity):
    def __init__(self, game, width, height):
        GameEntity.__init__(self, game, width, height)
        self.image = self.game.sprite_sheet.get_image(PLAYER_HUMAN[0],
                                                      PLAYER_HUMAN[1],
                                                      PLAYER_HUMAN[2],
                                                      PLAYER_HUMAN[3])
        self.rect = self.image.get_rect()
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(0, 0)

    def update(self):
        pass


class World:
    def __init__(self):
        self.world_coords_origin = vec(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2))
        self.world_coords_offset = (0, 0)

    def update_coords(self, vector_object):
        self.world_coords_offset = vector_object
        pass

    def retrieve_coords(self):
        return self.world_coords_offset


# Everything will blit to surface and the surface will render to the screen
class RenderSurface(pg.Surface):
    def __init__(self, game, width=SURFACE_WIDTH, height=SURFACE_HEIGHT):
        pg.Surface.__init__(self, (width, height))
        self.game = game
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width, self.height))
        self.image = self.image.convert()
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        # self.game.screen.blit(self.image, self.rect)
