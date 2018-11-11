# MechWarrior is an overhead real-time strategy/survival rpg
# import pygame as pg
# from settings import *
from Pawns import *
from Entity import Spritesheet
from World import *
from os import path
import os



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
        self.playing = True
        self.dir = None
        self.world = None
        self.load_assets()
        self.game_over = False

    def load_assets(self):
        # logging.info("Loading Assets...")
        self.world = World()
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "img")
        self.world.sprite_sheet = Spritesheet(path.join(img_dir, SPRITE_FILE_NAME))
        self.world.new()

    def new(self):
        # logging.info("Starting new game...")
        self.run()

    def run(self):
        # logging.info("Entering Game Loop...")
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.world.update()
            self.draw()
        # logging.info("Exiting Game Loop...")

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False


    def update(self):
        self.world.all_sprites.update()
        self.world.player_sprite.update()

    def draw(self):
        # Game Loop - Draw
        self.screen.fill(BLACK)
        self.world.all_sprites.draw(self.screen)
        self.world.player_sprite.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        print("Press \"n\" to start a new game or \"q\" to quit.")
        self.playing = False
        self.screen.fill(BLACK)
        while not self.playing:
            self.clock.tick(FPS)
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = True
                    self.running = False
            if keys[pg.K_n]:
                self.playing = True
            if keys[pg.K_q]:
                self.playing = True
                self.running = False

    def show_game_over_screen(self):
        # game over screen
        print("GAMEOVER")
        print("Press \"n\" to restart the game or \"q\" to quit.")
        self.screen.fill(BLACK)
        while not self.playing:
            self.clock.tick(FPS)
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = True
                    self.running = False
            if keys[pg.K_n]:
                self.playing = True
            if keys[pg.K_q]:
                self.playing = True
                self.running = False

g = Game()
while g.running:
    g.show_start_screen()
    g.new()
    if g.game_over:
        g.show_game_over_screen()
pg.quit()
# logging.info("Quitting Game...")
quit()
