from Pawns import *
from Entity import *
vec = pg.math.Vector2


class World:
    def __init__(self):
        self.world_coords_origin = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
        self.world_coords_offset = (0, 0)
        self.player_1 = None
        self.player_sprite = None
        self.sprite_sheet = None
        self.all_sprites = None
        self.offset_x = None
        self.offset_y = None
        self.floor_tile = None
        self.current_tiles = []
        self.render_surface = RenderSurface(self)

    def update_coords(self, vector_object):
        self.world_coords_offset = vector_object

    def retrieve_coords(self):
        return self.world_coords_offset

    def generate_additional_world(self):
        pass


    def update(self):
        self.player_1.update()
        previous_sprite_count = -1
        next_sprite_count = 1
        currCount = 0
        amount_tiles_wide = int(self.render_surface.rect.width / TILE_SIZE)
        for current_sprite in self.all_sprites.sprites():
            current_sprite.rect.x += int(self.player_1.vel.x + 0.5 * self.player_1.acc.x)
            current_sprite.rect.y += int(self.player_1.vel.y + 0.5 * self.player_1.acc.y)
        for current_sprite in self.all_sprites.sprites():
            position_modifier1 = currCount
            position_modifier2 = currCount
            if next_sprite_count == len(self.all_sprites):
                next_sprite_count = 0
            previous_sprite_x_right = self.all_sprites.sprites()[previous_sprite_count].rect.right
            next_sprite_x_left = self.all_sprites.sprites()[next_sprite_count].rect.left
            if current_sprite.rect.x < self.render_surface.rect.x:
                current_sprite.rect.x = previous_sprite_x_right
            if current_sprite.rect.right > self.render_surface.rect.x + self.render_surface.rect.width:
                current_sprite.rect.right = next_sprite_x_left
            if current_sprite.rect.top - 1 < self.render_surface.rect.y:
                for a in range(amount_tiles_wide):
                    position_modifier1 -= 1
                    if position_modifier1 == -1:
                        position_modifier1 = len(self.all_sprites.sprites()) - 1
                previous_sprite_y_bot = self.all_sprites.sprites()[position_modifier1].rect.bottom
                current_sprite.rect.top = previous_sprite_y_bot
            if current_sprite.rect.bottom > self.render_surface.rect.y + self.render_surface.rect.height:
                for b in range(amount_tiles_wide):
                    position_modifier2 += 1
                    if position_modifier2 == len(self.all_sprites):
                        position_modifier2 = 0
                next_sprite_y_top = self.all_sprites.sprites()[position_modifier2].rect.top
                current_sprite.rect.bottom = next_sprite_y_top
            previous_sprite_count += 1
            next_sprite_count += 1
            currCount += 1

    def new(self):
        self.all_sprites = pg.sprite.OrderedUpdates()
        self.player_sprite = pg.sprite.OrderedUpdates()
        for a in range(int(self.render_surface.rect.height / TILE_SIZE) + 1):
            for b in range(int(self.render_surface.rect.width / TILE_SIZE)):
                self.floor_tile = GameEntity(self, TILE_SIZE, TILE_SIZE, DESSERT)
                self.offset_x = (self.render_surface.rect.x + TILE_SIZE * b)
                self.offset_y = (self.render_surface.rect.y + TILE_SIZE * a)
                self.floor_tile.rect.x = self.offset_x
                self.floor_tile.rect.y = self.offset_y
                # self.render_surface.blit(self.floor_tile.image, (self.offset_x, self.offset_y), None)
                self.all_sprites.add(self.floor_tile)
        self.player_1 = Player(self, TILE_SIZE, TILE_SIZE)
        self.player_1.rect.center = self.render_surface.rect.center
        self.player_sprite.add(self.player_1)

class RenderSurface(pg.Surface):
    def __init__(self, game, width=SURFACE_WIDTH, height=SURFACE_HEIGHT):
        pg.Surface.__init__(self, (width, height))
        self.game = game
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        # self.game.screen.blit(self.image, self.rect)
