#sprite classes for platformer
import pygame as pg
from settings import *
from Entity import GameEntity
vec = pg.math.Vector2


# the player directly affects the camera, but the player is always centered in the camera
class Player(GameEntity):
    def __init__(self, world, width, height):
        GameEntity.__init__(self, world, width, height)
        self.image = self.world.sprite_sheet.get_image(PLAYER_HUMAN[0],
                                                      PLAYER_HUMAN[1],
                                                      PLAYER_HUMAN[2],
                                                      PLAYER_HUMAN[3])
        self.rect = self.image.get_rect()
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(0, 0)
        self.health = 100
        self.is_alive = True
        self.world = world
        self.rotation = 0
        self.rotation_speed = 5

    def update(self):
        self.get_keys()
        if self.health <= 0:
            self.alive = False
        if self.alive == False:
            print("Player Died, game over.")
            self.game.playing = False
            self.game.game_over = True

    def get_keys(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            pg.transform.rotate(self.image, self.rotation)
            self.acc.x = PLAYER_ACCELERATION
            if keys[pg.K_LSHIFT]:
                self.acc.x = PLAYER_ACCELERATION * 2
        if keys[pg.K_d]:
            self.acc.x = -PLAYER_ACCELERATION
            if keys[pg.K_LSHIFT]:
                self.acc.x = -PLAYER_ACCELERATION * 2
        if keys[pg.K_w]:
            self.acc.y = PLAYER_ACCELERATION
            if keys[pg.K_LSHIFT]:
                self.acc.y = PLAYER_ACCELERATION * 2
        if keys[pg.K_s]:
            self.acc.y = -PLAYER_ACCELERATION
            if keys[pg.K_LSHIFT]:
                self.acc.y = -PLAYER_ACCELERATION * 2
                # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc


class ItemBoost(GameEntity):
    def __init__(self):
        self.image = self.game.sprite_sheet.get_image(POWER_UP)


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
