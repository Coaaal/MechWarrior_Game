import pygame as pg
from config import settings
from entity import GameEntity
from objects import Weapon

vec = pg.math.Vector2


# the player directly affects the camera, but the player is always centered in the camera
class Player(GameEntity):
    def __init__(self, **kwargs):
        super(Player, self).__init__(sprite_atlas_coordinates=settings.SPRITE_ATLAS["PLAYER_HUMAN"], **kwargs)
        self.rect.center = (settings.APP.SCREEN_WIDTH / 2 - self.image.get_width() / 2,
                            settings.APP.SCREEN_HEIGHT / 2 - self.image.get_height() / 2)
        self.world = kwargs.get('world')
        self.health = 100
        self.rotation_speed = 5
        self.rotation_amount = 0
        self.is_alive = True
        self.weapons = []
        self.current_weapon = None
        self.x_off = 0
        self.y_off = 0
        self.override_velocity = False
        self.pickup_item()

    def pickup_item(self, *items):
        for item in items:
            if type(item) is Weapon:
                self.weapons += [item]
                self.current_weapon = item
                print('Picked up {}: {}'.format(type(item), item.name))

    def get_movement_vector(self):
        vel_x = int(self.vel.x + 0.5 * self.acc.x)
        vel_y = int(self.vel.y + 0.5 * self.acc.y)
        return vel_x, vel_y

    def update(self):
        print("Player Angle: {}".format(self.rotation_amount))
        self.get_keys()
        if self.health <= 0:
            self.is_alive = False

    def rotate(self, input_direction):
        if input_direction != self.rotation_amount:
            if self.rotation_amount > 350:
                self.rotation_amount = 0
            if self.rotation_amount < 0:
                self.rotation_amount = 350
            if (input_direction - self.rotation_amount - 360) % 360 < 180:
                self.rotation_amount += self.rotation_speed
            elif True:
                self.rotation_amount -= self.rotation_speed
            rot_image = pg.transform.rotate(self.image_copy, self.rotation_amount)
            self.rect.topleft = (
                settings.APP.SCREEN_WIDTH / 2 - rot_image.get_width() / 2, settings.APP.SCREEN_HEIGHT / 2 - rot_image.get_height() / 2)
            self.image = rot_image

    def shoot(self):
        self.current_weapon.shoot()

    def get_keys(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()
        acceleration_factor = 1
        if mouse[0]:
            self.shoot()
        if keys[pg.K_a]:
            if keys[pg.K_w]:
                self.rotate(45)
                acceleration_factor = 1.41
            elif keys[pg.K_s]:
                acceleration_factor = 1.41
                self.rotate(135)
            elif True:
                self.rotate(90)
            self.acc.x = settings.PLAYER["ACCELERATION"]
            if keys[pg.K_LSHIFT]:
                self.acc.x = settings.PLAYER["ACCELERATION"] * 2
        if keys[pg.K_d]:
            if keys[pg.K_s]:
                acceleration_factor = 1.41
                self.rotate(225)
            elif keys[pg.K_w]:
                acceleration_factor = 1.41
                self.rotate(315)
            elif True:
                self.rotate(270)
            self.acc.x = -settings.PLAYER["ACCELERATION"]
            if keys[pg.K_LSHIFT]:
                self.acc.x = -settings.PLAYER["ACCELERATION"] * 2
        if keys[pg.K_w]:
            if keys[pg.K_a]:
                acceleration_factor = 1.41
                self.rotate(45)
            elif keys[pg.K_d]:
                acceleration_factor = 1.41
                self.rotate(315)
            elif True:
                self.rotate(0)
            self.acc.y = settings.PLAYER["ACCELERATION"]
            if keys[pg.K_LSHIFT]:
                self.acc.y = settings.PLAYER["ACCELERATION"] * 2
        if keys[pg.K_s]:
            if keys[pg.K_a]:
                acceleration_factor = 1.41
                self.rotate(135)
            elif keys[pg.K_d]:
                acceleration_factor = 1.41
                self.rotate(225)
            elif True:
                self.rotate(180)
            self.acc.y = -settings.PLAYER["ACCELERATION"]
            if keys[pg.K_LSHIFT]:
                self.acc.y = -settings.PLAYER["ACCELERATION"] * 2
                # apply friction
        if keys[pg.K_k]:
            self.health = 0
        self.acc += (self.vel * settings.PLAYER["FRICTION"]) * acceleration_factor
        self.vel += self.acc
        if self.override_velocity:
            self.vel = -self.vel - self.acc
        # for sprite in self.world.object_sprites:
        #     if pg.sprite.spritecollide(self, sprite):
        #         self.vel = -self.vel
