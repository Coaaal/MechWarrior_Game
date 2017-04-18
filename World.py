import pygame as pg
from settings import *
vec = pg.math.Vector2

class World:
    def __init__(self):
        self.world_coords_origin = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
        self.world_coords_offset = (0, 0)

    def update_coords(self, vector_object):
        self.world_coords_offset = vector_object
        pass

    def retrieve_coords(self):
        return self.world_coords_offset


class GenerateAdditionalWorld:
    pass
