from entity import GameEntity
from config import settings


class Terrain(GameEntity):
    def __init__(self, **kwargs):
        super(Terrain, self).__init__(**kwargs)


class Dessert(Terrain):
    def __init__(self, sprite_atlas_coordinates=settings.SPRITE_ATLAS["DESSERT"], **kwargs):
        super(Dessert, self).__init__(sprite_atlas_coordinates=sprite_atlas_coordinates, **kwargs)
