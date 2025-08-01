import pygame
import const
import spriteSheet
import room
import math
import random
from pygame.math import Vector2

# Class for carts that can be pushed around
class Cart():
    # dir: direction where the cart is facing
    # pos: location on screen
    # roomDist: distance from the middle room (further away carts weigh more)
    def __init__(self, pos):
        self.dir = random.randint(0,3)
        cartSpriteSheet = pygame.image.load('images/cart.png').convert() # Load player's spritesheet
        self.cartSprite = spriteSheet.SpriteSheet(cartSpriteSheet)
        self.image = self.cartSprite.getImage(self.dir,38,38,const.scale)
        self.rect = self.image.get_rect(center = pos)
        self.pos = Vector2(self.rect.center)

    # Returns wheather the push was successfull
    def push(self, dir, vel, room):
        if dir != self.dir:
            self.newDir(dir)
        self.pos += vel*0.75
        return not self.resolveCollision(room)

    def newDir(self, dir):
        self.dir = dir
        self.image = self.cartSprite.getImage(dir,38,38,const.scale)
    
    def resolveCollision(self, room):
        self.rect.center = (self.pos.x, self.pos.y)
        solids = room.solidRects.copy()
        collided = False
        for solid in solids:                                # Check all the solid rects in the room
            if self.rect.colliderect(solid) and solid != self.rect:
                overlap = self.rect.clip(solid)             # Compute overlap rectangle
                if overlap.width < overlap.height : # Choose the smaller overlap dimension
                    if self.rect.centerx > solid.centerx:   # cart is on right side of tile -> push right
                        self.pos.x = solid.right + math.ceil(self.rect.width/2)
                    else:
                        self.pos.x = solid.left - math.ceil(self.rect.width/2)
                else:
                    if self.rect.centery > solid.centery:   # cart is below tile -> push down
                        self.pos.y = solid.bottom + math.ceil(self.rect.height/2)
                    else:
                        self.pos.y = solid.top - math.ceil(self.rect.height/2)
                self.rect.center = (self.pos.x, self.pos.y)
                collided = True
        return collided

    def updatePos(self, screenMove):
        newPos = (self.rect[0] + screenMove[0]/2 + 19, self.rect[1] + screenMove[1]/2 + 19)
        self.image = self.cartSprite.getImage(self.dir,38,38,const.scale)
        self.rect = self.image.get_rect(center = newPos)
        self.pos = Vector2(self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)