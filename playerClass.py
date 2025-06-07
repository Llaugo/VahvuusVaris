import pygame
import constants
import spriteSheet
import button

# Player class tracking movement and walking animations.
class Player(pygame.sprite.Sprite):
    # controls: Consists of four control buttons (d,r,u,l) of the Button class
    def __init__(self, controls: tuple[button.Button,button.Button,button.Button,button.Button]):
        super().__init__()
        playerSpriteSheet = pygame.image.load('images/player_sheet_ph.png').convert() # Load player's spritesheet
        self.playerSprite = spriteSheet.SpriteSheet(playerSpriteSheet)
        self.image = self.playerSprite.getImage(0,32,46,constants.scale)
        self.facing = 0 # 0,1,2,3 = down,right,up,left
        self.walking = 0 # When rounded 0 = standing, 1,2,3 = walking
        self.rect = self.image.get_rect(midbottom = (constants.worldWidth/2, constants.worldHeight/2))
        self.controls = controls
        
    # Tracks for each movement key/button if they are pressed and updates the direction the
    # player is facing and moves the walking animation value up.
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] or self.controls[0].activated: # Down key/button
            self.facing = 0
            self.walking = (self.walking + constants.playerSpeed/20.0) % 4
            self.rect.y += constants.playerSpeed
        elif keys[pygame.K_RIGHT] or self.controls[1].activated: # Right key/button
            self.facing = 1
            self.walking = (self.walking + constants.playerSpeed/20.0) % 4
            self.rect.x += constants.playerSpeed
        elif keys[pygame.K_UP] or self.controls[2].activated: # Up key/button
            self.facing = 2
            self.walking = (self.walking + constants.playerSpeed/20.0) % 4
            self.rect.y -= constants.playerSpeed
        elif keys[pygame.K_LEFT] or self.controls[3].activated: # Left key/button
            self.facing = 3
            self.walking = (self.walking + constants.playerSpeed/20.0) % 4
            self.rect.x -= constants.playerSpeed
        else:
            self.walking = 0 # If no buttons are pressed, we want the first picture of the animation (standing)
        animationFrame = self.facing*4 + round(self.walking) % 4
        self.image = self.playerSprite.getImage(animationFrame,32,46,constants.scale)

    def update(self):
        self.player_input()