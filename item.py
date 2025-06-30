import pygame
import const
import picture
import spriteSheet
import random

class Item():
    # pos: location of the item
    # roomDistance: How far away the room/item is from the middle. Far away rooms produce rarer items.
    def __init__(self, pos, roomDistance=0):
        #self.pos = pos
        self.color = random.randint(0,3)*4
        self.shinePhase = 0 # Goes from 0 to 4
        itemSpriteSheet = pygame.image.load('images/item_sheet.png').convert() # Load items' spritesheet
        self.itemSprite = spriteSheet.SpriteSheet(itemSpriteSheet)
        self.image = self.itemSprite.getImage(self.color,35,35,const.scale)
        self.rect = self.image.get_rect(center = pos)
        self.name = self.rollItem(roomDistance)

    def updatePos(self, pos):
        self.rect.center = pos

    def draw(self, screen):
        self.shinePhase += 0.1 
        self.image = self.itemSprite.getImage(self.color + (round(self.shinePhase) % 4),35,35,const.scale)
        screen.blit(self.image, self.rect)

    def rollItem(self,roomDistance):
        randomFloat = random.random()
        for i in range(len(const.itemRarity[roomDistance])):
            if randomFloat <= const.itemRarity[roomDistance][i]:
                return const.shop[i][random.randint(0,4)]
        raise ValueError('Could not determine item based on rarity level.')
        

