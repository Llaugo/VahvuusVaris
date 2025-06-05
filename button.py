import pygame
import spriteSheet

class Button():
    # ButtonType is indexed number equating to interface_sheet.png
    # pos is a double for the x and y coordinates of the button center
    def __init__(self, buttonType, pos, scale, screen):
        buttonSpriteSheet = pygame.image.load('images/interface_sheet.png').convert() # Load buttons spritesheet
        self.buttonSprite = spriteSheet.SpriteSheet(buttonSpriteSheet)
        self.buttonType = buttonType
        self.scale = scale
        self.image = self.buttonSprite.getImage(self.buttonType,46,46,self.scale,(0,0,0))
        self.rect = self.image.get_rect(center = pos)
        self.activated = 0 # Is the button being pressed

    def press(self):
        self.activated = 1
        self.image = self.buttonSprite.getImage(self.buttonType+1,46,46,self.scale,(0,0,0))
    
    def unpress(self):
        self.activated = 0
        self.image = self.buttonSprite.getImage(self.buttonType,46,46,self.scale,(0,0,0))

    def draw(self, screen):
        screen.blit(self.image, (self.rect))

