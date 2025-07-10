import pygame
import const
import picture
import spriteSheet
import text
import random

class Item():
    # pos: location of the item
    # roomDistance: How far away the room/item is from the middle. Far away rooms produce more rarer items.
    def __init__(self, pos, roomDistance=0):
        self.picType = random.randint(0,3)*4 # Randomize item image
        self.shinePhase = 0 # Goes from 0 to 4 (Animation helper)
        itemSpriteSheet = pygame.image.load('images/item_sheet.png').convert() # Load items' spritesheet
        self.itemSprite = spriteSheet.SpriteSheet(itemSpriteSheet)
        self.image = self.itemSprite.getImage(self.picType,35,35,const.scale)
        self.rect = self.image.get_rect(center = pos)
        self.name = self.rollItem(roomDistance) # Determine item name/type
        self.text = text.Text(const.sGameFont,self.name,pos,(46, 49, 79)) # Item name as text

    # Update item pos
    def updatePos(self, pos):
        self.rect.center = pos

    # Draw item with animated shine effect
    def draw(self, screen):
        self.shinePhase += 0.1 
        self.image = self.itemSprite.getImage(self.picType + (round(self.shinePhase) % 4),35,35,const.scale)
        screen.blit(self.image, self.rect)

    # Set the name/type of the item randomly
    def rollItem(self,roomDistance):
        randomFloat = random.random()
        for i in range(len(const.itemRarity[roomDistance])): # Get item rarities according to the room distance
            if randomFloat <= const.itemRarity[roomDistance][i]: # Compare rarity list to the random float
                return const.shop[i][random.randint(0,4)]
        raise ValueError('Could not determine item based on rarity level.')
        

