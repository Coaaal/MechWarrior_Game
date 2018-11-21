from game_entities import pawn, terrain, objects
import pygame as pg
from config import settings
from pygame import Surface, sprite
import random
vec = pg.math.Vector2


class World:
    def __init__(self):
        self.world_coords_origin = settings.APP.SCREEN_WIDTH/2, settings.APP.SCREEN_HEIGHT/2
        self.world_coords_offset = vec(0, 0)
        self.player_1 = None
        self.player_sprite = sprite.Group()
        self.terrain_sprites = sprite.OrderedUpdates()
        self.effects = sprite.Group()
        self.projectile_sprites = sprite.Group()
        self.object_sprites = sprite.Group()
        self.offset_x = None
        self.offset_y = None
        self.render_surface = RenderSurface(width=settings.GAME.SURFACE_WIDTH, height=settings.GAME.SURFACE_HEIGHT)
        self.amount_tiles_wide = int(self.render_surface.rect.width / settings.TILE.DIMENSION)
        self.p_move_vector = None

    def update_coords(self, vector_object):
        self.world_coords_offset -= vector_object / settings.TILE.DIMENSION

    def generate_additional_world(self):
        pass

    def spawn_item(self, **kwargs):
        if 'projectile' in kwargs:
            self.projectile_sprites.add(kwargs.get('projectile'))
        if 'effect' in kwargs:
            print('spawning effect')
            effect = kwargs.get('effect')
            effect.rect.x = kwargs.get('spawn_coordinates')[0]
            effect.rect.y = kwargs.get('spawn_coordinates')[1]
            self.effects.add(kwargs.get('effect'))

    def update(self):
        self.p_move_vector = self.player_1.get_movement_vector()
        self.object_sprites.update()
        if pg.sprite.spritecollide(self.player_1, self.object_sprites, False):
            self.player_1.override_velocity = True
        else:
            self.player_1.override_velocity = False
        self.player_sprite.update()
        self.projectile_sprites.update()
        for object_sprite in self.object_sprites:
            pg.sprite.spritecollide(object_sprite, self.projectile_sprites, True)
        self.effects.update()
        self.update_world()

    def update_world(self):
        previous_sprite_count = -1
        next_sprite_count = 1
        current_count = 0
        for current_sprite in self.terrain_sprites.sprites():
            current_sprite.rect.x += self.p_move_vector[0]
            current_sprite.rect.y += self.p_move_vector[1]
        for current_sprite in self.terrain_sprites.sprites():
            position_modifier1 = current_count
            position_modifier2 = current_count
            if next_sprite_count == len(self.terrain_sprites):
                next_sprite_count = 0
            previous_sprite_x_right = self.terrain_sprites.sprites()[previous_sprite_count].rect.right
            next_sprite_x_left = self.terrain_sprites.sprites()[next_sprite_count].rect.left
            if current_sprite.rect.x < self.render_surface.rect.x:
                current_sprite.rect.x = previous_sprite_x_right
            if current_sprite.rect.right > self.render_surface.rect.x + self.render_surface.rect.width:
                current_sprite.rect.right = next_sprite_x_left
            if current_sprite.rect.top - 1 < self.render_surface.rect.y:
                for a in range(self.amount_tiles_wide):
                    position_modifier1 -= 1
                    if position_modifier1 == -1:
                        position_modifier1 = len(self.terrain_sprites.sprites()) - 1
                previous_sprite_y_bot = self.terrain_sprites.sprites()[position_modifier1].rect.bottom
                current_sprite.rect.top = previous_sprite_y_bot
            if current_sprite.rect.bottom > self.render_surface.rect.y + self.render_surface.rect.height:
                for b in range(self.amount_tiles_wide):
                    position_modifier2 += 1
                    if position_modifier2 == len(self.terrain_sprites):
                        position_modifier2 = 0
                next_sprite_y_top = self.terrain_sprites.sprites()[position_modifier2].rect.top
                current_sprite.rect.bottom = next_sprite_y_top
            previous_sprite_count += 1
            next_sprite_count += 1
            current_count += 1
        self.update_coords(self.player_1.vel)

    def new(self):
        self.player_1 = pawn.Player(world=self, name="Player 1")
        self.player_1.rect.center = self.render_surface.rect.center
        new_weapon = objects.Weapon(owner=self.player_1, name="armBlaster")
        self.player_1.pickup_item(new_weapon)
        self.player_sprite.add(self.player_1)

        spawn_angles = [0, 90, 180, 270]
        for a in range(int(self.render_surface.rect.height / settings.TILE.DIMENSION)):
            for b in range(int(self.render_surface.rect.width / settings.TILE.DIMENSION)):
                floor_tile = terrain.Dessert()
                self.offset_x = (self.render_surface.rect.x + settings.TILE.DIMENSION * b)
                self.offset_y = (self.render_surface.rect.y + settings.TILE.DIMENSION * a)
                floor_tile.rect.x = self.offset_x
                floor_tile.rect.y = self.offset_y
                floor_tile.rotate(spawn_angles[random.randint(0, 3)])
                # self.render_surface.blit(self.floor_tile.image, (self.offset_x, self.offset_y), None)
                self.terrain_sprites.add(floor_tile)
                if a in [3, 4, 5, 6, 7] or b in [4, 6, 8]:
                    wall = objects.Wall(player_ref=self.player_1, name=(a * b))
                    wall.rect.x = a * settings.TILE.DIMENSION
                    wall.rect.y = b * settings.TILE.DIMENSION
                    self.object_sprites.add(wall)


class RenderSurface(Surface):
    def __init__(self, **kwargs):
        super(Surface, self).__init__(**kwargs)
        self.image = Surface((kwargs.get('width'), kwargs.get('height')))
        self.rect = self.image.get_rect()
        self.rect.center = [settings.APP.SCREEN_WIDTH/2, settings.APP.SCREEN_HEIGHT/2]
        # self.game.screen.blit(self.image, self.rect)
