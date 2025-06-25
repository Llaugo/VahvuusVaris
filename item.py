import pygame
import const
import picture
import spriteSheet
from random import randint

class Item():
    def __init__(self, pos):
        #self.pos = pos
        self.color = randint(0,3)*4
        self.shinePhase = 0 # Goes from 0 to 4
        itemSpriteSheet = pygame.image.load('images/item_sheet.png').convert() # Load items' spritesheet
        self.itemSprite = spriteSheet.SpriteSheet(itemSpriteSheet)
        self.image = self.itemSprite.getImage(self.color,35,35,const.scale)
        self.rect = self.image.get_rect(center = pos)


    def updatePos(self, pos):
        self.rect.center = pos

    def draw(self, screen):
        self.shinePhase += 0.1 
        self.image = self.itemSprite.getImage(self.color + (round(self.shinePhase) % 4),35,35,const.scale)
        screen.blit(self.image, self.rect)