#sprite classes for platformer
import pygame as pg
from settings import *
from Entity import GameEntity
from os import path
import json
import inspect
import logging
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
        self.rect.center = (SCREEN_WIDTH / 2 - self.image.get_width() / 2, SCREEN_HEIGHT / 2 - self.image.get_height() / 2)
        self.image_copy = self.image.copy()
        self.copy_rect = self.image_copy.get_rect()
        self.player_center = self.copy_rect.center
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(0, 0)
        self.health = 100
        self.width = width
        self.rotation_speed = 10
        self.rotation_amount = 0
        self.is_alive = True
        self.world = world
        self.weapons = []
        self.current_weapon = None
        self.x_off = 0
        self.y_off = 0
        self.pickup_item()



    def pickup_item(self):
        print("picking up arm_blaster")
        new_weapon = Weapon(self, self.world, name="arm_blaster")
        self.weapons.append(new_weapon)
        self.current_weapon = new_weapon
        print(self.current_weapon.name)
        print(self.current_weapon.damage)
        # self.weapons.append

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
            self.rect.topleft = (SCREEN_WIDTH/2 - rot_image.get_width()/2, SCREEN_HEIGHT/2 - rot_image.get_height()/2)
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
    def __init__(self, player, world, name):
        self.world = world
        self.image = self.world.sprite_sheet.get_image(WEAPON[0],
                                                      WEAPON[1],
                                                      WEAPON[2],
                                                      WEAPON[3])
        self.player = player
        self.name = name
        self.bullet_speed = 0
        self.ammo_type = 0
        self.total_ammo = 0
        self.current_ammo_amount = 0
        self.shoot_speed = 0
        self.reload_speed = 0
        self.damage = 0
        self.level = 0
        self.distance = 0
        self.weapons_dir = (((path.dirname(path.abspath(inspect.getfile(inspect.currentframe()))))) + "\weapons.json")
        self.setup_weapon()
        self.live_bullets = []

    def get_keys(self):
        mouse_event = pg.mouse.get_pressed()
        if mouse_event[0]:  #  and self.current_ammo > 0
            self.shoot()

    def shoot(self):
        print("shooting at players rotation of :", self.player.rotation_amount)
        current_bullet = Bullet(self.world)
        self.live_bullets.append(current_bullet)

    def update(self):
        print("BLAHHHH")
    def reloading(self):
        pass

    def set_ammo_type(self):
        pass

    def setup_weapon(self):
        json_data = open(self.weapons_dir).read()
        weapon_list = json.loads(json_data)
        found_weapon = weapon_list[self.name]
        self.distance = found_weapon["Distance"]
        self.level = found_weapon["Level"]
        self.damage = found_weapon["Damage"]
        self.ammo_type = found_weapon["AmmoType"]
        self.current_ammo_amount = found_weapon["CurrentAmmoAmount"]
        self.total_ammo = found_weapon["TotalAmmo"]
        self.bullet_speed = found_weapon["BulletSpeed"]
        self.reload_speed = found_weapon["ReloadSpeed"]


class Bullet(GameEntity):
    def __init__(self, world):
        self.world = world
        self.image = self.world.sprite_sheet.get_image(BULLET[0],
                                                       BULLET[1],
                                                       BULLET[2],
                                                       BULLET[3])
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(0, 0)
        self.is_alive = True
