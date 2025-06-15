import pygame
from settings import *
from support import *



class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.import_assets()  # Load animations and assets
        self.status = 'down_idle'
        self.frame_index = 0

        #sprite image, general setup
        self.image = pygame.Surface((32,64))
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    #movement attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = PLAYER_SPEED

    def input(self):
        #basic movement input handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def move(self, dt):
        # Normalize the direction vector to prevent faster diagonal movement
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()


        #horizontal movement
        if self.direction.x != 0:
            self.pos.x += self.direction.x * self.speed * dt
            # Check for collision with screen boundaries
            if self.pos.x < 0:
                self.pos.x = 0
            elif self.pos.x > SCREEN_WIDTH - self.rect.width:
                self.pos.x = SCREEN_WIDTH - self.rect.width
        
        #vertical movement
        if self.direction.y != 0:
            self.pos.y += self.direction.y * self.speed * dt
            # Check for collision with screen boundaries
            if self.pos.y < 0:
                self.pos.y = 0
            elif self.pos.y > SCREEN_HEIGHT - self.rect.height:
                self.pos.y = SCREEN_HEIGHT - self.rect.height

        #position and speed (collision)
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def import_assets(self):
        #update these with new animations
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [], 'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [], 'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [], 'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}

        for animation in self.animations.keys():
            full_path = f'graphics/old_graphics/character/{animation}'
            self.animations[animation] = import_folder(full_path)

    
    def update(self, dt):
        self.input()
        self.move(dt)