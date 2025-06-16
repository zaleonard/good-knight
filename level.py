import pygame
from settings import *
from player import Player
from overlay import *
from sprites import Generic
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface() #level draws straight onto main display
        # self.player = Player()

        #sprite groups
        self.all_sprites = CameraGroup()
        
        self.setup()
        self.overlay = Overlay(self.player)
    
    def setup(self):
        # Load the Tiled map
        tmx_data = load_pygame('C:/Users/zaleo/OneDrive/Desktop/good_knight/graphics/old_graphics/tmx/imports_data/map.tmx')

        #house
        for x, y, surf in tmx_data.get_layer_by_name('HouseFurnitureBottom').tiles():
            Generic(
                pos = (x * TILE_SIZE, y * TILE_SIZE),
                surf = surf,
                groups = self.all_sprites,
                z=LAYERS['house bottom']
            )


        # Load background or level elements here if needed
        Generic(
            pos = (0, 0),
            surf = pygame.image.load('graphics/old_graphics/world/ground.png').convert_alpha(),
            groups = self.all_sprites,
            z=LAYERS['ground']
        )
        self.player=Player((640, 360), self.all_sprites) #pos is tuple iwth x and y

    def run(self,dt):
        self.display_surface.fill(BACKGROUND_COLOR)
        self.all_sprites.customize_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()



        # self.player.update(dt)

#camera for sprite scrolling
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def customize_draw(self, player):

        #ensures player is always centered on screen
        self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    # Calculate the offset position for the sprite
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset


                    self.display_surface.blit(
                        sprite.image,
                        offset_rect
                    )