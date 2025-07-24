import pygame
import const
import spriteSheet

# Class for advert screens that shoot the player and push them back
class Advert():
    # dir: initial direction of the advert
    def __init__(self, dir):
        advertSpriteSheet = pygame.image.load('images/advert_screen.png').convert() # Load tile spritesheet
        self.advertSprite = spriteSheet.SpriteSheet(advertSpriteSheet)
        self.dir = dir
        self.image = self.advertSprite.getImage(dir,30,30,const.scale)
        self.rect = self.image.get_rect()

    def updatePos(self, pos):
        self.rect.center = pos

    # amount: how many 90 degree turns, positive integers clockwise
    def rotate(self, amount):
        self.dir = (self.dir + amount) % 4
        self.image = self.advertSprite.getImage(self.dir,30,30,const.scale)