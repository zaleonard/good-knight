import pygame
from settings import *
from player import Player

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface() #level draws straight onto main display
        # self.player = Player()

        #sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.setup()

    
    def setup(self):
        self.player=Player((640, 360), self.all_sprites) #pos is tuple iwth x and y

    def run(self,dt):
        self.display_surface.fill('black')  # Clear the screen with black color
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)




        # self.player.update(dt)