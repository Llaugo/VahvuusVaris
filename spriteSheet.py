import pygame

# Class for extracting single image sprites from a spritesheet.
class SpriteSheet():
    def __init__(self, sheet):
        self.sheet = sheet
    
    # Get a certain image from a line of sprites
    # frame: Image index on the spritesheet
    # width, height: dimensions of the image on the sheet. Width should be the same for all images in a sheet
    # scale: Image scale on the screen
    # color: Needed for keying transparent images (default is black)
    def getImage(self, frame, width, height, scale, color = (0,0,0)):
        image = pygame.Surface((width,height)).convert()
        image.blit(self.sheet, (0,0), (frame*width, 0, width, height))
        image = pygame.transform.scale(image, (width*scale,height*scale))
        image.set_colorkey(color)
        return image
    