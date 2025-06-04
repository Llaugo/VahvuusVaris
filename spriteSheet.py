import pygame

class SpriteSheet():
    def __init__(self, sheet):
        self.sheet = sheet
    
    def getImage(self, frame, width, height, scale, color):
        image = pygame.Surface((width,height)).convert()
        image.blit(self.sheet, (0,0), ((frame*width), 0, width, height))
        image = pygame.transform.scale(image, (width*scale,height*scale))
        image.set_colorkey(color)
        return image
    