import pygame
import const
import spriteSheet
from pygame.math import Vector2

# Class for advert screens that shoot the player and push them back
class Advert():
    # dir: initial direction of the advert
    def __init__(self, dir):
        advertSpriteSheet = pygame.image.load('images/advert_screen.png').convert() # Load tile spritesheet
        self.advertSprite = spriteSheet.SpriteSheet(advertSpriteSheet)
        self.dir = dir
        self.image = self.advertSprite.getImage(dir,30,30,const.scale)
        self.rect = self.image.get_rect()
        self.streamEnd = self.rect.center

    def update(self, player, room):
        # Push player to the direction if player is in front
        if self.dir == 0 and player.rect.collidepoint((self.streamEnd[0],player.pos[1])) and self.streamEnd[1] > player.pos[1] > self.rect.centery:
                player.push(const.basePlayerSpeed, Vector2(0,1), room)
        elif self.dir == 1 and player.rect.collidepoint((player.pos[0],self.streamEnd[1])) and self.streamEnd[0] > player.pos[0] > self.rect.centerx:
                player.push(const.basePlayerSpeed, Vector2(1,0), room)
        elif self.dir == 2 and player.rect.collidepoint((self.streamEnd[0],player.pos[1])) and self.streamEnd[1] < player.pos[1] < self.rect.centery:
                player.push(const.basePlayerSpeed, Vector2(0,-1), room)
        elif self.dir == 3 and player.rect.collidepoint((player.pos[0],self.streamEnd[1])) and self.streamEnd[0] < player.pos[0] < self.rect.centerx:
                player.push(const.basePlayerSpeed, Vector2(-1,0), room)


    def updatePos(self, pos):
        self.rect.center = pos

    def setEnd(self, pos):
        self.streamEnd = pos

    # amount: how many 90 degree turns, positive integers clockwise
    def rotate(self, amount):
        self.dir = (self.dir + amount) % 4
        self.image = self.advertSprite.getImage(self.dir,30,30,const.scale)