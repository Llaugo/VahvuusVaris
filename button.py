import pygame
import spriteSheet
import text

# Class for making buttons that can be pressed down and used by other things
class Button():
    # buttonType: The number just tells what image to use in the interface_sheet.png
    # pos: A double for the x and y coordinates of the button center
    # scale: For determining the image size
    def __init__(self, buttonType, pos, scale, font=None, buttonText="Test button", color=(0,0,0)):
        buttonSpriteSheet = pygame.image.load('images/interface_sheet.png').convert() # Load buttons spritesheet
        self.buttonSprite = spriteSheet.SpriteSheet(buttonSpriteSheet)
        self.buttonType = buttonType
        self.scale = scale
        self.image = self.buttonSprite.getImage(self.buttonType,100,100,self.scale)
        self.rect = self.image.get_rect(center = pos)
        self.activated = 0 # Tracks if this button is pressed
        self.text = None
        if font:
            self.text = text.Text(font, buttonText, pos, color)
            self.text.updatePos(pos, True)

    # Press this button
    def press(self):
        self.activated = 1
        self.image = self.buttonSprite.getImage(self.buttonType+1,100,100,self.scale) # Update pressed button image
    
    # Unpress this button
    def unpress(self):
        self.activated = 0
        self.image = self.buttonSprite.getImage(self.buttonType,100,100,self.scale) # Update lifted button image

    # pos: new pos of the button
    def updatePos(self, pos):
        self.rect.center = pos
        if self.text:
            self.text.updatePos(pos, True)

    # Draws this button on the screen
    def draw(self, screen):
        screen.blit(self.image, (self.rect))
        if self.text:
            self.text.draw(screen)

