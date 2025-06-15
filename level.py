import pygame
from settings import *

class Level:
    def __init__(self):
        self.player = Player()
    def run(self,dt):
        self.player.update(dt)