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
        self.activeFinger = None
        self.text = None
        if font:
            self.text = text.Text(font, buttonText, pos, color)
            self.text.updatePos(pos, True)

    # Press this button
    def press(self, fingerID):
        self.activeFinger = fingerID
        self.image = self.buttonSprite.getImage(self.buttonType+1,100,100,self.scale) # Update pressed button image
    
    # Unpress this button
    def unpress(self):
        self.activeFinger = None
        self.image = self.buttonSprite.getImage(self.buttonType,100,100,self.scale) # Update lifted button image

    # pos: new pos of the button
    def updatePos(self, pos):
        self.rect.center = pos
        if self.text:
            self.text.updatePos(pos, True)

    def handleEvent(self, event, screenSize):
        # Track touch
        if event.type == pygame.FINGERDOWN:
            if self.rect.collidePoint(event.x*screenSize[0], event.y*screenSize[1]):
                self.press(event.finger_id)
                return True
        elif event.type == pygame.FINGERUP and event.finger_id == self.activeFinger:
            self.unpress()
            return True
        # Track mouse
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.press("mouse")
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.activeFinger:
            self.unpress()
            return True
        return False

    # Draws this button on the screen
    def draw(self, screen):
        screen.blit(self.image, (self.rect))
        if self.text:
            self.text.draw(screen)

