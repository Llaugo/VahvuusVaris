import pygame
import spriteSheet
import text

# Class for making buttons that can be pressed down and used by other things
class Button():
    # buttonNum: The number just tells what image to use in the spritesheet
    # type: What type of button this is (0=movement button, other=width of the button)
    # pos: A double for the x and y coordinates of the button center
    # scale: For determining the image size
    # font: The font of the text on the button. If not specified, no text is displayed
    # buttonText: Text on the button
    # color: Color of the button text. Black by default
    def __init__(self, buttonNum, type, pos, scale, font=None, buttonText="Test button", color=(0,0,0)):
        self.buttonNum = buttonNum
        self.scale = scale
        self.type = type
        if self.type == 4:
            buttonSpriteSheet = pygame.image.load('images/buttons_l.png').convert() # Load buttons spritesheet
        else:
            buttonSpriteSheet = pygame.image.load('images/buttons_s.png').convert() # Load buttons spritesheet
        self.buttonSprite = spriteSheet.SpriteSheet(buttonSpriteSheet)
        if not self.type: self.image = self.buttonSprite.getImage(self.buttonNum,100,100,self.scale)
        else: self.image = self.buttonSprite.getImage(self.buttonNum,100*self.type,100,self.scale)
        self.rect = self.image.get_rect(center = pos)
        self.activeFinger = None # Id of the pressing finger
        self.pressComplete = False
        self.text = None # Text on the button
        if font: # If font is specified, render text on the button
            self.text = text.Text(font, buttonText, pos, color)
            self.text.updatePos(pos, True)

    # Press this button
    def press(self, fingerID):
        self.activeFinger = fingerID
        if not self.type:
            self.pressComplete = True
        if not self.type: self.image = self.buttonSprite.getImage(self.buttonNum+1,100,100,self.scale)
        else: self.image = self.buttonSprite.getImage(self.buttonNum+1,100*self.type,100,self.scale) # Update pressed button image

    def release(self):
        self.activeFinger = None
        self.pressComplete = True
    
    # Unpress this button
    def unpress(self):
        self.activeFinger = None
        self.pressComplete = False
        if not self.type: self.image = self.buttonSprite.getImage(self.buttonNum,100,100,self.scale)
        else: self.image = self.buttonSprite.getImage(self.buttonNum,100*self.type,100,self.scale) # Update lifted button image

    # pos: new pos of the button
    def updatePos(self, pos):
        self.rect.center = pos
        if self.text: # Update text pos
            self.text.updatePos(pos, True)

    # Track button pressing
    def handleEvent(self, event, screenSize):
        if not self.type:
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
        else:
            # Track touch
            if event.type == pygame.FINGERDOWN:
                if self.rect.collidePoint(event.x*screenSize[0], event.y*screenSize[1]):
                    self.press(event.finger_id)
                    return True
            elif event.type == pygame.FINGERUP and event.finger_id == self.activeFinger:
                self.release()
                return True
            # Track mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.press("mouse")
                    return True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.activeFinger:
                self.release()
                return True
            return False

    # Draws this button on the screen
    def draw(self, screen):
        screen.blit(self.image, (self.rect))
        if self.text: # Draw text on top
            self.text.draw(screen)

