import pygame
import const
import spriteSheet
from pygame.math import Vector2

# A class for a non-playable character
class Npc():
    # dir: initial facing direction
    def __init__(self, pos, dir):
        self.pos: Vector2 = pos
        self.baseDir = dir
        self.facing = dir
        npcSpriteSheet = pygame.image.load('images/npc_sheet.png').convert() # Load player's spritesheet
        self.npcSprite = spriteSheet.SpriteSheet(npcSpriteSheet)
        self.image = self.npcSprite.getImage(self.facing*4,36,41,const.scale)
        self.rect = self.image.get_rect(center = self.pos)
        self.pos = Vector2(self.rect.center)
        self.speed = const.npcWalkSpeed
        self.strength = 100
        self.walkDuration = 0
        self.walking = 0        # Animation helper
        self.tradedWith = False

    def trade(self):
        self.tradedWith = True

    # Return True if teleport was successful, False if collision happened
    def teleport(self, newPos, room):
        oldPos = self.pos
        self.setPos(newPos)
        solids = room.solidRects.copy()
        solids += room.waterRects
        for npc in room.npcs:
            if npc != self:
                solids.append(npc.rect)
        for cart in room.carts:
            solids.append(cart.rect)
        collided = False
        for solid in solids:
            if self.rect.colliderect(solid):
                collided = True
                break
        if collided:
            self.setPos(oldPos)
        return not collided
    
    def walk(self, duration):
        self.walkDuration = duration

    def turn(self, faceDir):
        self.facing = faceDir
        self.image = self.npcSprite.getImage(self.facing*4,36,41,const.scale)

    # Go back to facing basic direction
    # dir: If set, make dir the basic direction
    def turnBack(self, dir=None):
        if dir != None:
            self.baseDir = dir
        self.turn(self.baseDir)

    def updatePos(self, screenMove):
        self.setPos((self.rect[0] + screenMove[0]/2 + 18, self.rect[1] + screenMove[1]/2 + 17))

    def setPos(self, pos):
        self.pos = Vector2(pos)
        self.resetRect()

    def resetRect(self):
        self.rect.height = 35
        self.rect.center = self.pos

    def update(self, room, player):
        if self.walkDuration == 1:
            self.walking = 0
            self.image = self.npcSprite.getImage(self.facing*4 + round(self.walking) % 4,36,41,const.scale)
        self.walkDuration = max(self.walkDuration-1, 0)
        if self.walkDuration:
            velocity = Vector2()
            if self.facing == 0:
                velocity += Vector2(0,1)
            elif self.facing == 1:
                velocity += Vector2(1,0)
            elif self.facing == 2:
                velocity += Vector2(0,-1)
            elif self.facing == 3:
                velocity += Vector2(-1,0)
            if not velocity:
                self.walking = 0
            else:
                self.pos += (velocity*self.speed)
                self.rect.center = (self.pos.x, self.pos.y)
                if not room.collideCarts(self, self.facing, (velocity*self.speed), player):
                    self.pos -= (velocity*self.speed)
                    self.rect.center = (self.pos.x, self.pos.y)
                    self.walk(0)
                    self.walking = 0
                self.walking = (self.walking + self.speed/20.0) % 4
            animationFrame = self.facing*4 + round(self.walking) % 4 # Get the correct image (frame of the animation)
            self.image = self.npcSprite.getImage(animationFrame,36,41,const.scale)
            
    # Draw the npc on the screen
    def draw(self, screen):
        drawRect = self.rect.copy()
        drawRect.y -= 12
        screen.blit(self.image, drawRect)