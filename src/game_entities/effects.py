from entity import SpriteAnimation


class Explosion(SpriteAnimation):
    def __init__(self, **kwargs):
        super(Explosion, self).__init__(**kwargs)
        self.player_ref = kwargs.get('player_ref')

    def update(self, *args):
        movement_vector = self.player_ref.get_movement_vector()
        self.rect.x = self.rect.x + movement_vector[0]
        self.rect.y = self.rect.y + movement_vector[1]
        self.next_frame()
