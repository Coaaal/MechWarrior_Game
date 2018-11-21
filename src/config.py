from addict import Dict
from sprite_atlas import get_sprite_atlas, get_explosion_atlas
import logging
import yaml
import os

settings_path = os.path.join(os.path.split(__file__)[0], 'settings\default.yaml')

#  ToDo: Move all processing folders to a processing directory so that they are a bit more hidden and better structured
PROJECT_MODE = os.environ.get('PROJECTMODE')


with open(settings_path, 'r') as f:
    settings = Dict(yaml.load(f))

if PROJECT_MODE is not None:
    with open('settings\{}.yaml'.format(PROJECT_MODE), 'r') as f:
        settings.update(yaml.load(f))


logging.info('Project Mode is currently set to: {}'.format(PROJECT_MODE))

settings.update({"SPRITE_ATLAS": get_sprite_atlas(settings.TILE.DIMENSION)})
settings.update({"EXPLOSION_ATLAS": get_explosion_atlas(settings.TILE.DIMENSION)})
