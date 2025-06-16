import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.import_assets()  # Load animations and assets
        self.status = 'down_idle'
        self.frame_index = 0

        #sprite image, general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['main']


        #movement attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = PLAYER_SPEED

        #timers
        self.timers = {
            'tool_use': Timer(350, self.use_tool), #dont call function just pass it
            'tool_switch': Timer(200),
            'seed_use': Timer(350, self.use_seed),
            'seed_switch': Timer(200),
        }
        self.tools = ['axe', 'hoe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]  # Default tool

        #seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]  # Default seed

    def use_tool(self):
        pass
        # print(f'Using {self.selected_tool} tool')
        # Implement tool usage logic here
        # For example, you could check the player's position and interact with the environment

    def use_seed(self):
        pass
        # print(f'Using {self.selected_seed} seed')
        # Implement seed usage logic here
        # For example, you could check the player's position and plant the seed in the environment

    def import_assets(self):
        #update these with new animations
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [], 'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [], 'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [], 'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}

        for animation in self.animations.keys():
            full_path = f'graphics/old_graphics/character/{animation}'
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt  # Adjust the speed of animation
         # Loop through the animation frames
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]


    def input(self):
        #basic movement input handling
        keys = pygame.key.get_pressed()

        if not self.timers['tool_use'].active:  # Only process movement if tool is not in use
        #directions
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            
            #tool selection
            if keys[pygame.K_SPACE]:
                self.timers['tool_use'].activate()
                self.direction = pygame.math.Vector2(0, 0)  # Stop movement while using tool
                self.frame_index = 0  # Reset animation frame index

            #change tools
            if keys[pygame.K_q] and not self.timers['tool_switch'].active:
                self.timers['tool_switch'].activate()
                self.tool_index += 1
                if self.tool_index >= len(self.tools):
                    self.tool_index = 0
                self.selected_tool = self.tools[self.tool_index]

            #seed selection
            if keys[pygame.K_LCTRL]:
                self.timers['seed_use'].activate()
                self.direction = pygame.math.Vector2(0, 0)  # Stop movement while using tool
                self.frame_index = 0  # Reset animation frame index
                # print(f'selected seed: {self.selected_seed}')

            #change seeds
            if keys[pygame.K_e] and not self.timers['seed_switch'].active:
                self.timers['seed_switch'].activate()
                self.seed_index += 1
                if self.seed_index >= len(self.seeds):
                    self.seed_index = 0
                self.selected_seed = self.seeds[self.seed_index]
                # print(f'changed seed: {self.selected_seed}')

    def get_status(self):
        #if the player is not moving, add _idle to the status
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        if self.timers['tool_use'].active:
            self.status = self.status.split('_')[0] + f'_{self.selected_tool}'

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()


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
            # elif self.pos.x > SCREEN_WIDTH - self.rect.width:
            #     self.pos.x = SCREEN_WIDTH - self.rect.width
        
        #vertical movement
        if self.direction.y != 0:
            self.pos.y += self.direction.y * self.speed * dt
            # Check for collision with screen boundaries
            if self.pos.y < 0:
                self.pos.y = 0
            # elif self.pos.y > SCREEN_HEIGHT - self.rect.height:
            #     self.pos.y = SCREEN_HEIGHT - self.rect.height

        #position and speed (collision)
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos


    
    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        self.update_timers()