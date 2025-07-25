import pygame
import const
import spriteSheet

class Picture():
    # pic:  image path to load
    def __init__(self, pic, dimensions, pos, scale=const.scale):
        picSpriteSheet = pygame.image.load(pic).convert() # Load picture's spritesheet
        self.playerSprite = spriteSheet.SpriteSheet(picSpriteSheet)
        self.image = self.playerSprite.getImage(0,dimensions[0],dimensions[1],scale)
        self.rect = self.image.get_rect(center = pos)

    # Update the pos of the picture
    def updatePos(self, pos):
        self.rect = self.image.get_rect(center = (pos))

    # Draws the image on the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)