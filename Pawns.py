#sprite classes for platformer
import pygame as pg
from settings import *
from Entity import GameEntity
vec = pg.math.Vector2


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


# Everything will blit to surface and the surface will render to the screen
class RenderSurface(pg.Surface):
    def __init__(self, game,
                 width=SURFACE_WIDTH,
                 height=SURFACE_HEIGHT):
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
