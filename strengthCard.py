import pygame
import const
import spriteSheet

class StrengthCard():
    # imageNum: the index of the card image
    # pos: location of the card
    def __init__(self, imageNum):
        cardSpriteSheet = pygame.image.load('images/strength_sheet.png').convert() # Load strength spritesheet
        self.cardSprite = spriteSheet.SpriteSheet(cardSpriteSheet)
        self.image = self.cardSprite.getImage(imageNum,250,350,const.scale/2)