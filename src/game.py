# MechWarrior is an overhead real-time strategy/survival rpg
from application import Application
from config import settings
from world import World
import pygame as pg


class Game(Application):
    def __init__(self, name="MechWarrior", **kwargs):
        super(Game, self).__init__(name=name, **kwargs)
        # initialize game window etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode([settings.APP.SCREEN_WIDTH, settings.APP.SCREEN_HEIGHT])
        pg.display.set_caption(settings.APP.TITLE)
        self.clock = pg.time.Clock()
        self.tile_count_x = (settings.APP.SCREEN_WIDTH / settings.TILE.DIMENSION)
        self.tile_count_y = (settings.APP.SCREEN_HEIGHT / settings.TILE.DIMENSION)
        self.running = True
        self.playing = True
        self.world = None
        self.game_over = False

    def load_assets(self):
        # logging.info("Loading Assets...")
        self.world = World()
        self.world.new()

    def new(self):
        self.load_assets()
        # logging.info("Starting new game...")
        self.run()

    def run(self):
        super(Game, self).run()
        # logging.info("Entering Game Loop...")
        while self.playing:
            self.clock.tick(settings.GAME.FPS)
            self.events()
            self.update()
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
        self.world.update()

    def draw(self):
        # Game Loop - Draw
        self.screen.fill(settings.COLORS.BLACK)
        self.world.terrain_sprites.draw(self.screen)
        self.world.object_sprites.draw(self.screen)
        self.world.player_sprite.draw(self.screen)
        self.world.projectile_sprites.draw(self.screen)
        self.world.effects.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        print("Press \"n\" to start a new game or \"q\" to quit.")
        self.playing = False
        self.screen.fill(settings.COLORS.BLACK)
        while not self.playing:
            self.clock.tick(settings.GAME.FPS)
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
        self.screen.fill(settings.COLORS.BLACK)
        while not self.playing:
            self.clock.tick(settings.GAME.FPS)
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


if __name__ == "__main__":
    game_session = Game()
    while game_session.running:
        game_session.show_start_screen()
        game_session.new()
        if game_session.game_over:
            game_session.show_game_over_screen()

pg.quit()
# logging.info("Quitting Game...")
quit()
