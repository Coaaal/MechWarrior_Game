from Pawns import *
from Entity import *
from pygame import Surface, sprite
vec = pg.math.Vector2


class World:
    def __init__(self):
        self.world_coords_origin = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
        self.world_coords_offset = (0, 0)
        self.player_1 = None
        self.player_sprite = sprite.OrderedUpdates()
        self.sprite_sheet = None
        self.terrain_sprites = sprite.OrderedUpdates()
        self.projectile_sprites = sprite.OrderedUpdates()
        self.offset_x = None
        self.offset_y = None
        self.current_tiles = []
        self.render_surface = RenderSurface(game=self, width=SURFACE_WIDTH, height=SURFACE_HEIGHT)

    def update_coords(self, vector_object):
        self.world_coords_offset = vector_object

    def retrieve_coords(self):
        return self.world_coords_offset

    def generate_additional_world(self):
        pass

    def spawn_item(self, item):
        item.rect.x, item.rect.y = self.player_1.rect.x, self.player_1.rect.y
        self.projectile_sprites.add(item)

    def update(self):
        for player_sprites in self.player_sprite:
            player_sprites.update()
        previous_sprite_count = -1
        next_sprite_count = 1
        current_count = 0
        amount_tiles_wide = int(self.render_surface.rect.width / TILE_SIZE)
        for current_sprite in self.terrain_sprites.sprites():
            current_sprite.rect.x += int(self.player_1.vel.x + 0.5 * self.player_1.acc.x)
            current_sprite.rect.y += int(self.player_1.vel.y + 0.5 * self.player_1.acc.y)
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
                for a in range(amount_tiles_wide):
                    position_modifier1 -= 1
                    if position_modifier1 == -1:
                        position_modifier1 = len(self.terrain_sprites.sprites()) - 1
                previous_sprite_y_bot = self.terrain_sprites.sprites()[position_modifier1].rect.bottom
                current_sprite.rect.top = previous_sprite_y_bot
            if current_sprite.rect.bottom > self.render_surface.rect.y + self.render_surface.rect.height:
                for b in range(amount_tiles_wide):
                    position_modifier2 += 1
                    if position_modifier2 == len(self.terrain_sprites):
                        position_modifier2 = 0
                next_sprite_y_top = self.terrain_sprites.sprites()[position_modifier2].rect.top
                current_sprite.rect.bottom = next_sprite_y_top
            previous_sprite_count += 1
            next_sprite_count += 1
            current_count += 1
        for projectile_sprite in self.projectile_sprites:
            projectile_sprite.update()

    def new(self):
        for a in range(int(self.render_surface.rect.height / TILE_SIZE) + 1):
            for b in range(int(self.render_surface.rect.width / TILE_SIZE)):
                floor_tile = GameEntity(world=self, asset_type=DESSERT, name="Dessert Tile")
                self.offset_x = (self.render_surface.rect.x + TILE_SIZE * b)
                self.offset_y = (self.render_surface.rect.y + TILE_SIZE * a)
                floor_tile.rect.x = self.offset_x
                floor_tile.rect.y = self.offset_y
                # self.render_surface.blit(self.floor_tile.image, (self.offset_x, self.offset_y), None)
                self.terrain_sprites.add(floor_tile)
        self.player_1 = Player(world=self, asset_type=PLAYER_HUMAN, name="Player 1")
        self.player_1.rect.center = self.render_surface.rect.center
        self.player_sprite.add(self.player_1)
        self.player_sprite.add(Weapon(player=self.player_1, world=self, name="armBlaster", asset_type=WEAPON))


class RenderSurface(Surface):
    def __init__(self, **kwargs):
        super(Surface, self).__init__(**kwargs)
        self.game = kwargs.get('game')
        self.image = Surface((kwargs.get('width'), kwargs.get('height')))
        self.rect = self.image.get_rect()
        self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        # self.game.screen.blit(self.image, self.rect)
