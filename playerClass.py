import pygame
import constants

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = constants.playerImg[0][0]
        self.facing = 0 # 0,1,2,3 = down,right,up,left
        self.walking = 0 # 0 = standing, 1,2,3 = walking
        self.rect = self.image.get_rect(midbottom = (constants.worldWidth/2, constants.worldHeight/2))
        

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.facing = 0
            self.walking = (self.walking + constants.playerSpeed/20.0) % 4
            self.rect.y += constants.playerSpeed
        elif keys[pygame.K_RIGHT]:
            self.facing = 1
            self.walking = (self.walking + constants.playerSpeed/20.0) % 4
            self.rect.x += constants.playerSpeed
        elif keys[pygame.K_UP]:
            self.facing = 2
            self.walking = (self.walking + constants.playerSpeed/20.0) % 4
            self.rect.y -= constants.playerSpeed
        elif keys[pygame.K_LEFT]:
            self.facing = 3
            self.walking = (self.walking + constants.playerSpeed/20.0) % 4
            self.rect.x -= constants.playerSpeed
        else:
            self.walking = 0
        self.image = constants.playerImg[self.facing][round(self.walking)%4]


    def update(self):
        self.player_input()