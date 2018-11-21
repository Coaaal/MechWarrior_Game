from entity import GameEntity
from config import settings
from effects import Explosion
from os import path
import pygame as pg
import json
vec = pg.math.Vector2


class Weapon(GameEntity):
    with open(path.join(path.dirname(__file__), 'weapons.json')) as f:
        all_weapons = json.load(f)

    def __init__(self, sprite_atlas_coordinates=settings.SPRITE_ATLAS["WEAPON"], **kwargs):
        super(Weapon, self).__init__(sprite_atlas_coordinates=sprite_atlas_coordinates, **kwargs)
        self.weapon_stats = None
        self.owner = kwargs.get('owner')
        self.setup_weapon()
        self.last_bullet = None

    def shoot(self):
        if not self.last_bullet:
            self.last_bullet = Bullet(weapon=self, life_length=self.weapon_stats['lifeLength'],
                                      bullet_speed=self.weapon_stats['bulletSpeed'], name=("{} ammo".format(self.name)),
                                      spawn_angle=self.owner.rotation_amount)
            self.owner.world.spawn_item(projectile=self.last_bullet)
        elif pg.time.get_ticks() - self.last_bullet.spawn_time > self.weapon_stats['millisecondsBetweenBullets']:
            self.last_bullet = Bullet(weapon=self, life_length=self.weapon_stats['lifeLength'],
                                      bullet_speed=self.weapon_stats['bulletSpeed'], name=("{} ammo".format(self.name)),
                                      spawn_angle=self.owner.rotation_amount)
            self.owner.world.spawn_item(projectile=self.last_bullet)

    def update(self):
        pass

    def reloading(self):
        pass

    def set_ammo_type(self):
        pass

    def setup_weapon(self):
        self.weapon_stats = Weapon.all_weapons.get(self.name)


class Wall(GameEntity):

    def __init__(self, sprite_atlas_coordinates=settings.SPRITE_ATLAS["WALL"], **kwargs):
        super(Wall, self).__init__(sprite_atlas_coordinates=sprite_atlas_coordinates, **kwargs)
        self.player_ref = kwargs.get('player_ref')

    def update(self):
        movement_vector = self.player_ref.get_movement_vector()
        self.rect.x = self.rect.x + movement_vector[0]
        self.rect.y = self.rect.y + movement_vector[1]


class Bullet(GameEntity):
    def __init__(self, sprite_atlas_coordinates=settings.SPRITE_ATLAS["BULLET"], **kwargs):
        super(Bullet, self).__init__(sprite_atlas_coordinates=sprite_atlas_coordinates, **kwargs)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(0, 0)
        self.image_copy = self.image.copy()
        self.copy_rect = self.image_copy.get_rect()
        self.rotation_amount = kwargs.get('spawn_angle')
        self.life_length = kwargs.get('life_length')
        self.speed = kwargs.get('bullet_speed')
        self.weapon = kwargs.get('weapon')
        self.x_movement = 0
        self.y_movement = 0
        self.rotate_image()
        self.set_movement()

    def set_movement(self):
        if self.rotation_amount < 0:
            self.rotation_amount = 360 + self.rotation_amount
        if 180 > self.rotation_amount >= 0:
            self.x_movement = -1 * (1 - (abs(90 - self.rotation_amount) / 90.0))
            self.y_movement = -1 * ((90 - self.rotation_amount) / 90.0)
        if 360 >= self.rotation_amount >= 180:
            self.x_movement = 1 - (abs(270 - self.rotation_amount) / 90.0)
            self.y_movement = ((270 - self.rotation_amount) / 90.0)
        self.x_movement = (self.x_movement * self.speed)
        self.y_movement = (self.y_movement * self.speed)

    def update(self):
        if (pg.time.get_ticks() - self.spawn_time) > self.life_length:
            self.kill()
        self.rect.x += self.x_movement
        self.rect.y += self.y_movement
        # self.rect.x, self.rect.y = self.pos

    def rotate_image(self):
        rot_image = pg.transform.rotate(self.image_copy, self.rotation_amount)
        self.rect.topleft = (
            settings.APP.SCREEN_WIDTH / 2 - rot_image.get_width() / 2, settings.APP.SCREEN_HEIGHT / 2 - rot_image.get_height() / 2)
        self.image = rot_image

    def kill(self):
        rect_x_death = self.rect.x
        rect_y_death = self.rect.y
        super(Bullet, self).kill()
        self.weapon.owner.world.spawn_item(effect=Explosion(player_ref=self.weapon.owner), spawn_coordinates=[rect_x_death, rect_y_death])
