import pygame
import const
import spriteSheet

class Picture():
    # pic:  image path to load
    def __init__(self, pic, dimensions, pos, scale=const.scale):
        picSpriteSheet = pygame.image.load(pic).convert() # Load picture's spritesheet
        self.playerSprite = spriteSheet.SpriteSheet(picSpriteSheet)
        self.dimensions = dimensions
        self.image = self.playerSprite.getImage(0,dimensions[0],dimensions[1],scale)
        self.rect = self.image.get_rect(center = pos)

    def blitOnto(self, surf, loc, relativeMid=False):
        if relativeMid:
            location = self.dimensions[0]/2 + loc[0], self.dimensions[1]/2 + loc[1]
        else:
            location = loc
        self.image.blit(surf, location)

    # Update the pos of the picture
    def updatePos(self, pos):
        self.rect = self.image.get_rect(center = (pos))

    # Draws the image on the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)