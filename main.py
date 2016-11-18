# MechWarrior is an overhead real-time strategy/survival rpg

# import pygame as pg
# from settings import *
from sprites import *
from os import path


class Game:
    def __init__(self):
        # initialize game window etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.tile_count_x = (SCREEN_WIDTH / TILE_SIZE)
        self.tile_count_y = (SCREEN_HEIGHT / TILE_SIZE)
        self.running = True
        self.playing = False
        self.dir = None
        self.sprite_sheet = None
        self.all_sprites = None
        self.offset_x = None
        self.offset_y = None
        self.floor_tile = None
        self.world_sprites = None
        self.render_surface = RenderSurface(self)
        self.acc = vec(0, 0)
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)

        self.load_assets()

    def load_assets(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "img")
        self.sprite_sheet = Spritesheet(path.join(img_dir, SPRITE_FILE_NAME))

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.OrderedUpdates()
        self.player_sprite = pg.sprite.OrderedUpdates()
        for a in range(int(self.render_surface.rect.height/TILE_SIZE) + 1):
            for b in range(int(self.render_surface.rect.width/TILE_SIZE)):
                self.floor_tile = GameEntity(self, TILE_SIZE, TILE_SIZE)
                self.offset_x = (self.render_surface.rect.x + TILE_SIZE * b)
                self.offset_y = (self.render_surface.rect.y + TILE_SIZE * a)
                self.floor_tile.rect.x = self.offset_x
                self.floor_tile.rect.y = self.offset_y
                # self.render_surface.blit(self.floor_tile.image, (self.offset_x, self.offset_y), None)
                self.all_sprites.add(self.floor_tile)
        self.player_1 = Player(self, TILE_SIZE, TILE_SIZE)
        self.player_1.rect.center = self.render_surface.rect.center
        self.player_sprite.add(self.player_1)
        # self.all_sprites.add(self.player_1)
        self.run()

    def run(self):
        # Game Loop

        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
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

    def update(self):
        # Game Loop - Update
        theCount = 1
        lastSprite = self.all_sprites.sprites()[-1]
        # !!!!!!!!!!! Need to set each sprite location
        # !!!!!!!!!!! To the one before its right side
        # !!!!!!!!!!! have to lose the vector
        previous_sprite_count = -1
        next_sprite_count = 1
        currCount = 0
        previous_height_sprite = int(self.render_surface.rect.width/TILE_SIZE)
        for current_sprite in self.all_sprites.sprites():
            current_sprite.rect.x += int(self.vel.x + 0.5 * self.acc.x)
            current_sprite.rect.y += int(self.vel.y + 0.5 * self.acc.y)
            # previous_sprite_x = (self.all_sprites.sprites()[previous_sprite_count].rect.right) + 1
            # if current_sprite.rect.x < self.render_surface.rect.x:
            #     current_sprite.rect.x = previous_sprite_x
            # if current_sprite.rect.x > self.render_surface.rect.x + SURFACE_WIDTH:
            #     current_sprite.rect.x = self.render_surface.rect.x
            # if current_sprite.rect.y < self.render_surface.rect.y:
            #     current_sprite.rect.y = self.render_surface.rect.y + SURFACE_HEIGHT
            # if current_sprite.rect.y > self.render_surface.rect.y + SURFACE_HEIGHT:
            #     current_sprite.rect.y = self.render_surface.rect.y
            # previous_sprite_count += 1
        for current_sprite in self.all_sprites.sprites():
            if next_sprite_count == len(self.all_sprites):
                next_sprite_count = 0
            previous_height_sprite = currCount - previous_height_sprite
            previous_sprite_x_right = (self.all_sprites.sprites()[previous_sprite_count].rect.right) + 1
            next_sprite_x_left = (self.all_sprites.sprites()[next_sprite_count].rect.left) - 1
            previous_sprite_y_bot = (self.all_sprites.sprites()[previous_height_sprite].rect.bottom) + 1
            # previous_sprite_x_bot = (self.all_sprites.sprites()[previous_sprite_count].rect.bottom) + 1
            if current_sprite.rect.x < self.render_surface.rect.x:
                current_sprite.rect.x = previous_sprite_x_right
            if current_sprite.rect.x > self.render_surface.rect.x + self.render_surface.rect.width:
                current_sprite.rect.right = next_sprite_x_left + 1
            if current_sprite.rect.y < self.render_surface.rect.y:
                current_sprite.rect.top = previous_sprite_y_bot
            if current_sprite.rect.y > self.render_surface.rect.y + self.render_surface.rect.height:
                current_sprite.rect.y = self.render_surface.rect.y
            previous_sprite_count += 1
            next_sprite_count += 1
            previous_height_sprite += 1
            currCount
            # self.render_surface.blit(self.floor_tile.image, (self.offset_x, self.offset_y), None)
        self.all_sprites.update()
        self.player_sprite.update()


    def draw(self):
        # Game Loop - Draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.player_sprite.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        # start screen
        pass

    def show_game_over_screen(self):
        # game over screen
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_game_over_screen()

pg.quit()
quit()
