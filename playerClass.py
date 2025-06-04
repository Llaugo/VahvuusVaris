import pygame
import constants
import spriteSheet

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        # self.screen = screen # Uncomment, if screen is needed elsewhere
        playerSpriteSheet = pygame.image.load('images/player_sheet_ph.png').convert() # Load player's spritesheet
        self.playerSprite = spriteSheet.SpriteSheet(playerSpriteSheet)
        self.image = self.playerSprite.getImage(0,32,46,constants.scale,(0,0,0))
        self.facing = 0 # 0,1,2,3 = down,right,up,left
        self.walking = 0 # When rounded 0 = standing, 1,2,3 = walking
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
        animationFrame = self.facing*4 + round(self.walking) % 4
        self.image = self.playerSprite.getImage(animationFrame,32,46,constants.scale,(0,0,0))


    def update(self):
        self.player_input()