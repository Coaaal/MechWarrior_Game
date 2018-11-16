import pygame as pg
from settings import *
from Entity import GameEntity
import math
import json

vec = pg.math.Vector2


# the player directly affects the camera, but the player is always centered in the camera
class Player(GameEntity):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.rect.center = (SCREEN_WIDTH / 2 - self.image.get_width() / 2,
                            SCREEN_HEIGHT / 2 - self.image.get_height() / 2)
        self.image_copy = self.image.copy()
        self.copy_rect = self.image_copy.get_rect()
        self.player_center = self.copy_rect.center
        self.health = 100
        self.rotation_speed = 10
        self.rotation_amount = 0
        self.is_alive = True
        self.weapons = []
        self.current_weapon = None
        self.x_off = 0
        self.y_off = 0
        self.pickup_item()

    def pickup_item(self):
        new_weapon = Weapon(owner=self, world=self.world, name="armBlaster", asset_type=WEAPON)
        self.weapons.append(new_weapon)
        self.current_weapon = new_weapon

    def get_movement_vector(self):
        vel_x = int(self.vel.x + 0.5 * self.acc.x)
        vel_y = int(self.vel.y + 0.5 * self.acc.y)
        return vel_x, vel_y

    def update(self):
        self.get_keys()
        if self.health <= 0:
            self.is_alive = False

    def rotate_player(self, input_direction):
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
            SCREEN_WIDTH / 2 - rot_image.get_width() / 2, SCREEN_HEIGHT / 2 - rot_image.get_height() / 2)
            self.image = rot_image

    def get_keys(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            if keys[pg.K_w]:
                self.rotate_player(45)
            elif keys[pg.K_s]:
                self.rotate_player(135)
            elif True:
                self.rotate_player(90)
            self.acc.x = PLAYER_ACCELERATION
            if keys[pg.K_LSHIFT]:
                self.acc.x = PLAYER_ACCELERATION * 2
        if keys[pg.K_d]:
            if keys[pg.K_s]:
                self.rotate_player(225)
            elif keys[pg.K_w]:
                self.rotate_player(315)
            elif True:
                self.rotate_player(270)
            self.acc.x = -PLAYER_ACCELERATION
            if keys[pg.K_LSHIFT]:
                self.acc.x = -PLAYER_ACCELERATION * 2
        if keys[pg.K_w]:
            if keys[pg.K_a]:
                self.rotate_player(45)
            elif keys[pg.K_d]:
                self.rotate_player(315)
            elif True:
                self.rotate_player(0)
            self.acc.y = PLAYER_ACCELERATION
            if keys[pg.K_LSHIFT]:
                self.acc.y = PLAYER_ACCELERATION * 2
        if keys[pg.K_s]:
            if keys[pg.K_a]:
                self.rotate_player(135)
            elif keys[pg.K_d]:
                self.rotate_player(225)
            elif True:
                self.rotate_player(180)
            self.acc.y = -PLAYER_ACCELERATION
            if keys[pg.K_LSHIFT]:
                self.acc.y = -PLAYER_ACCELERATION * 2
                # apply friction
        if keys[pg.K_k]:
            self.health = 0
        self.current_weapon.get_keys()
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc


# class ItemBoost(GameEntity):
#     def __init__(self):
#         self.image = self.game.sprite_sheet.get_image(POWER_UP)


class Weapon(GameEntity):
    with open('weapons.json') as f:
        all_weapons = json.load(f)

    def __init__(self, **kwargs):
        super(Weapon, self).__init__(**kwargs)
        self.weapon_stats = None
        self.owner = kwargs.get('owner')
        self.setup_weapon()
        self.last_bullet = None

    def get_keys(self):
        mouse_event = pg.mouse.get_pressed()
        if mouse_event[0]:  # and self.current_ammo > 0
            if not self.last_bullet:
                self.shoot()
            elif pg.time.get_ticks() - self.last_bullet.spawn_time > self.weapon_stats['millisecondsBetweenBullets']:
                self.shoot()

    def shoot(self):
        self.last_bullet = Bullet(world=self.world, life_length=self.weapon_stats['lifeLength'],
                                  bullet_speed=self.weapon_stats['bulletSpeed'], name=("{} ammo".format(self.name)),
                                  spawn_angle=self.owner.rotation_amount)
        self.world.spawn_item(self.last_bullet)
        # current_bullet = Bullet(self.world)
        # self.live_bullets.append(current_bullet)

    def update(self):
        pass
        # print("BLAHHHH")

    def reloading(self):
        pass

    def set_ammo_type(self):
        pass

    def setup_weapon(self):
        self.weapon_stats = Weapon.all_weapons.get(self.name)


class Bullet(GameEntity):
    def __init__(self, **kwargs):
        super(Bullet, self).__init__(asset_type=BULLET, **kwargs)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(0, 0)
        self.image_copy = self.image.copy()
        self.copy_rect = self.image_copy.get_rect()
        self.rotation_amount = kwargs.get('spawn_angle')
        self.life_length = kwargs.get('life_length')
        self.speed = kwargs.get('bullet_speed')
        self.x_movement = 0
        self.y_movement = 0
        self.rotate_image()
        self.set_movement(player_vector=kwargs.get('player_vector'))

    def set_movement(self, **kwargs):
        if self.rotation_amount < 0:
            self.rotation_amount = 360 + self.rotation_amount
        if 180 > self.rotation_amount >= 0:
            self.x_movement = -1 * (1 - (abs(90 - self.rotation_amount) / 90.0))
            self.y_movement = -1 * ((90 - self.rotation_amount) / 90.0)
        if 360 >= self.rotation_amount >= 180:
            self.x_movement = 1 - (abs(270 - self.rotation_amount) / 90.0)
            self.y_movement = ((270 - self.rotation_amount) / 90.0)
        self.x_movement = round(self.x_movement * self.speed)
        self.y_movement = round(self.y_movement * self.speed)

    def update(self, **kwargs):
        if (pg.time.get_ticks() - self.spawn_time) > self.life_length:
            self.kill()
        self.rect.x += self.x_movement
        self.rect.y += self.y_movement
        # self.rect.x, self.rect.y = self.pos

    def rotate_image(self):
        rot_image = pg.transform.rotate(self.image_copy, self.rotation_amount)
        self.rect.topleft = (
            SCREEN_WIDTH / 2 - rot_image.get_width() / 2, SCREEN_HEIGHT / 2 - rot_image.get_height() / 2)
        self.image = rot_image
