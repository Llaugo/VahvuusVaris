import pygame
import const
import spriteSheet
import room
import item
import math
import random
from pygame.math import Vector2

# Class for carts that can be pushed around
class Cart():
    # dir: direction where the cart is facing
    # pos: location on screen
    # dir: initial facing direction
    # lang: language of the game
    # roomDist: distance from the middle room (for item generation)
    def __init__(self, pos, dir, lang, roomDist):
        self.lang = lang
        self.dir = dir
        cartSpriteSheet = pygame.image.load('images/cart.png').convert() # Load player's spritesheet
        self.cartSprite = spriteSheet.SpriteSheet(cartSpriteSheet)
        self.image = self.cartSprite.getImage(self.dir,38,38,const.scale)
        self.rect = self.image.get_rect(center = pos)
        self.pos = Vector2(self.rect.center)
        self.roomDist = roomDist
        self.item = item.Item(self.pos, self.lang, min(self.roomDist+2, const.roomDistMax),12) # Items rarities in the carts are boosted by two rooms

    # Returns the old item
    def switchItem(self, newItem):
        oldItem = self.item
        addedItem = item.Item(self.pos, self.lang, 0, 12)
        addedItem.setName(newItem)
        addedItem.updatePos(self.pos)
        self.item = addedItem
        return oldItem

    # Returns wheather the push was successfull
    def push(self, dir, vel, room, pusher, player):
        if dir != self.dir:
            self.newDir(dir)
        if pusher == player:
            self.pos += vel*0.75
        else:
            self.pos += vel
        result = not self.resolveCollision(room, pusher, player)
        self.item.updatePos(self.pos)
        return result

    def newDir(self, dir):
        self.dir = dir
        self.image = self.cartSprite.getImage(dir,38,38,const.scale)
    
    def resolveCollision(self, room, pusher, player):
        self.rect.center = (self.pos.x, self.pos.y)
        solids = room.solidRects.copy()
        for npc in room.npcs:
            if npc != pusher:
                solids.append(npc.rect)
        if player != pusher:
            solids.append(player.rect)
        for door in room.doorways:
            solids.append(door)
        collided = False
        for solid in solids:                                # Check all the solid rects in the room
            if self.rect.colliderect(solid) and solid != self.rect:
                for door in room.doorways:
                    if door == solid:
                        player.speak(const.phrase[self.lang][60])
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
        self.item.updatePos(self.pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)