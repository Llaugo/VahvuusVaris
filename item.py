import pygame
import const
import picture
import spriteSheet
import text
import random

class Item():
    # pos: location of the item
    # lang: language of the game
    # roomDistance: How far away the room/item is from the middle. Far away rooms produce more rarer items.
    def __init__(self, pos, lang, roomDistance=0, fontSize=30):
        self.lang = lang
        self.picType = random.randint(0,3)*4 # Randomize item image
        self.shinePhase = 0 # Goes from 0 to 4 (Animation helper)
        itemSpriteSheet = pygame.image.load('images/item_sheet.png').convert() # Load items' spritesheet
        self.itemSprite = spriteSheet.SpriteSheet(itemSpriteSheet)
        self.image = self.itemSprite.getImage(self.picType,35,35,const.scale)
        self.rect = self.image.get_rect(center = pos)
        self.name = self.rollItem(roomDistance) # Determine item name/type
        self.text = text.Text(const.gameFont(fontSize),self.name,pos,(46, 49, 79),2,True) # Item name as text


    def setName(self, newName):
        self.name = newName
        self.text.setText(self.name)

    # Update item pos
    def updatePos(self, pos):
        self.rect.center = pos
        self.text.updatePos((pos[0],pos[1]+23))

    # Draw item with animated shine effect
    def draw(self, screen):
        oldShine = round(self.shinePhase)
        self.shinePhase += 0.1
        if oldShine != round(self.shinePhase):
            self.image = self.itemSprite.getImage(self.picType + (round(self.shinePhase) % 4),35,35,const.scale)
        screen.blit(self.image, self.rect)

    # Set the name/type of the item randomly
    def rollItem(self,roomDistance):
        randomFloat = random.random()
        for i in range(len(const.itemRarity[roomDistance])): # Get item rarities according to the room distance
            if randomFloat <= const.itemRarity[roomDistance][i]: # Compare rarity list to the random float
                return const.shop(self.lang)[i][random.randint(0,4)]
        raise ValueError('Could not determine item based on rarity level.')
        

