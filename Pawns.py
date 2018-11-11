import pygame as pg
from settings import *
from Entity import GameEntity
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
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(0, 0)
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
        new_weapon = Weapon(player=self, world=self.world, name="armBlaster", asset_type=WEAPON)
        print("picking up item: {}".format(new_weapon.name))
        self.weapons.append(new_weapon)
        self.current_weapon = new_weapon

    def update(self):
        self.get_keys()
        if self.health <= 0:
            self.alive = False
        if self.alive == False:
            print("Player Died, game over.")
            self.game.playing = False
            self.game.game_over = True

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
        self.name = kwargs.get('name')
        self.weapon_stats = None
        self.live_bullets = []
        self.setup_weapon()

    def get_keys(self):
        mouse_event = pg.mouse.get_pressed()
        if mouse_event[0]:  # and self.current_ammo > 0
            self.shoot()

    def shoot(self):
        print("{} just shot!".format(self.name))
        # current_bullet = Bullet(self.world)
        # self.live_bullets.append(current_bullet)

    def update(self):
        print("BLAHHHH")

    def reloading(self):
        pass

    def set_ammo_type(self):
        pass

    def setup_weapon(self):
        self.weapon_stats = Weapon.all_weapons.get(self.name)


class Bullet(GameEntity):
    def __init__(self, **kwargs):
        super(Bullet, self).__init__(asset_type=BULLET, **kwargs)
        self.world = kwargs.get('world')
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(0, 0)
        self.is_alive = True
