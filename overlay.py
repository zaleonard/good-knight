import pygame
from settings import *
import os

class Overlay:
    def __init__(self, player):

        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        #imports
        overlay_path = 'graphics/old_graphics/overlay'
        self.tools_surf = {tool:pygame.image.load(f'{overlay_path}/{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surf = {seed:pygame.image.load(f'{overlay_path}/{seed}.png').convert_alpha() for seed in player.seeds}