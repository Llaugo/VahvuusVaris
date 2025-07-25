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
        self.stream = self.rect

    def update(self, player, room):
        # Push player to the direction if player is in front
        if player.rect.colliderect(self.stream):
            if self.dir == 0:
                player.push(const.basePlayerSpeed*1.5, Vector2(0,1), room)
            elif self.dir == 1:
                player.push(const.basePlayerSpeed*1.5, Vector2(1,0), room)
            elif self.dir == 2:
                player.push(const.basePlayerSpeed*1.5, Vector2(0,-1), room)
            elif self.dir == 3:
                player.push(const.basePlayerSpeed*1.5, Vector2(-1,0), room)


    def updatePos(self, pos):
        self.rect.center = pos
        if self.dir == 0:
            self.stream.midtop = self.rect.midtop
        elif self.dir == 1:
            self.stream.midleft = self.rect.midleft
        elif self.dir == 2:
            self.stream.midbottom = self.rect.midbottom
        elif self.dir == 3:
            self.stream.midright = self.rect.midright

    # pos: Endpoint of the stream
    def setStream(self, pos):
        self.streamEnd = pos
        if self.dir == 0:
            self.stream = pygame.Rect(0,0,const.tileSize,abs(self.rect.top-pos[1]))
            self.stream.midtop = self.rect.midtop
        elif self.dir == 1:
            self.stream = pygame.Rect(0,0,abs(self.rect.left-pos[0]),const.tileSize)
            self.stream.midleft = self.rect.midleft
        elif self.dir == 2:
            self.stream = pygame.Rect(0,0,const.tileSize,abs(self.rect.bottom-pos[1]))
            self.stream.midbottom = self.rect.midbottom
        elif self.dir == 3:
            self.stream = pygame.Rect(0,0,abs(self.rect.right-pos[0]),const.tileSize)
            self.stream.midright = self.rect.midright
        #print(self.stream.topleft,self.stream.bottomright)
        #print(self.rect.center)


    # amount: how many 90 degree turns, positive integers clockwise, negative counterclockwise
    def rotate(self, amount):
        self.dir = (self.dir + amount) % 4
        self.image = self.advertSprite.getImage(self.dir,30,30,const.scale)
        self.stream = self.rect