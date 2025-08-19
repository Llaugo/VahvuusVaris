import pygame

# Class for extracting single image sprites from a spritesheet.
class SpriteSheet():
    def __init__(self, sheet):
        try:
            self.sheet = pygame.image.load(sheet).convert()
        except Exception as e:
            print("ASSET LOAD FAILED:", e)
        self.store = {}
    
    # Get a certain image from a line of sprites
    # frame: Image index on the spritesheet
    # width, height: dimensions of the image on the sheet. Width should be the same for all images in a sheet
    # scale: Image scale on the screen
    # color: Needed for keying transparent images (default is black)
    def getImage(self, frame, width, height, scale, color = (1,0,0)):
        #key = self.sheet.get_at((frame*width, 0))
        storekey = (frame, width, height, scale, color)
        if storekey in self.store:
            return self.store[storekey]
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet, (0,0), (frame*width, 0, width, height))
        #image.set_colorkey(color)
        if scale != 1:
            image = pygame.transform.scale(image, (width*scale,height*scale))
        self.store[storekey] = image
        return image
    