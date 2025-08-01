import pygame
import const
import spriteSheet
import random
from pygame.math import Vector2

# Class for carts that can be pushed around
class Cart():
    def __init__(self, dir, pos, roomDist):
        self.dir = dir
        self.weight = roomDist
        cartSpriteSheet = pygame.image.load('images/cart.png').convert() # Load player's spritesheet
        self.cartSprite = spriteSheet.SpriteSheet(cartSpriteSheet)
        self.image = self.cartSprite.getImage(dir,38,38,const.scale)
        self.rect = self.image.get_rect(center = pos)
        self.pos = Vector2(self.rect.center)

    def updatePos(self, screenMove):
        newPos = (self.rect[0] + screenMove[0]/2 + 19, self.rect[1] + screenMove[1]/2 + 19)
        self.image = self.cartSprite.getImage(self.dir,38,38,const.scale)
        self.rect = self.image.get_rect(center = newPos)
        self.pos = Vector2(self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)