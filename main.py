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

        self.load_assets()

    def load_assets(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "img")
        self.sprite_sheet = Spritesheet(path.join(img_dir, SPRITE_FILE_NAME))

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player_sprite = pg.sprite.LayeredUpdates()
        for a in range(int(self.render_surface.rect.height/TILE_SIZE)):
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


    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.player_sprite.update()
        print(str(self.render_surface.rect.width))

    def draw(self):
        # Game Loop - Draw
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
