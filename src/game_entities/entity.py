import pygame as pg
from os import path
from config import settings

vec = pg.math.Vector2


class SpriteSheet:
    # loads and parses sprite sheets
    def __init__(self, **kwargs):
        self.sprite_sheet = pg.image.load(path.join(path.join(path.dirname(path.dirname(__file__)), "img"),
                                                    kwargs.get('sheet')))

    def get_image(self, x, y, width, height):
            my_image = pg.Surface((width, height), pg.SRCALPHA)  # , pg.SRCALPHA, 32
            my_image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
            return my_image

    # def get_rect(self):


basic_sheet = SpriteSheet(sheet=settings.SPRITESHEET.BASIC)
explosion_sheet = SpriteSheet(sheet=settings.SPRITESHEET.EXPLOSION)


class GameEntity(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        super(GameEntity, self).__init__()
        # pg.sprite.Sprite.__init__(self)
        self.world = kwargs.get('world')
        self.name = kwargs.get('name')
        self.width = settings.TILE.DIMENSION
        self.height = settings.TILE.DIMENSION
        self.sprite_atlas_coordinates = kwargs.get('sprite_atlas_coordinates')
        self.image = basic_sheet.get_image(self.sprite_atlas_coordinates[0],
                                           self.sprite_atlas_coordinates[1],
                                           self.sprite_atlas_coordinates[2],
                                           self.sprite_atlas_coordinates[3])
        self.image_copy = self.image.copy()
        self.copy_rect = self.image_copy.get_rect()
        self.rect = self.image.get_rect()
        self.rotation_amount = 0
        self.prev_rect_center = self.rect.center
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(0, 0)
        self.spawn_time = pg.time.get_ticks()

    def rotate(self, rotation_amount):
        self.prev_rect_center = self.rect.center
        if rotation_amount != self.rotation_amount:
            self.rotation_amount = rotation_amount
            rot_image = pg.transform.rotate(self.image_copy, rotation_amount)
            self.image = rot_image
            self.rect.center = self.prev_rect_center


class SpriteAnimation(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        super(SpriteAnimation, self).__init__()
        self.frame_count = len(settings.EXPLOSION_ATLAS["FRAMES"])
        self.image = explosion_sheet.get_image(settings.EXPLOSION_ATLAS["FRAMES"][0][0],
                                               settings.EXPLOSION_ATLAS["FRAMES"][0][1],
                                               settings.EXPLOSION_ATLAS["FRAMES"][0][2],
                                               settings.EXPLOSION_ATLAS["FRAMES"][0][3])
        self.width = settings.TILE.DIMENSION
        self.height = settings.TILE.DIMENSION
        self.rect = self.image.get_rect()
        self.last_time_played = pg.time.get_ticks()
        self.frame_speed = 1000
        self.current_frame = 0

    def next_frame(self):
        current_tick = pg.time.get_ticks()
        if self.last_time_played + 20 < current_tick:
            self.current_frame += 1
            if self.current_frame is self.frame_count - 1:
                self.kill()
            self.image = explosion_sheet.get_image(settings.EXPLOSION_ATLAS["FRAMES"][self.current_frame][0],
                                                   settings.EXPLOSION_ATLAS["FRAMES"][self.current_frame][1],
                                                   settings.EXPLOSION_ATLAS["FRAMES"][self.current_frame][2],
                                                   settings.EXPLOSION_ATLAS["FRAMES"][self.current_frame][3])
            self.last_time_played = current_tick

