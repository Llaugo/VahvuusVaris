import pygame
import const
import spriteSheet
from pygame.math import Vector2

# A class for a non-playable character
class Npc():
    # dir: initial facing direction
    def __init__(self, pos, dir):
        self.pos = pos
        self.baseDir = dir
        self.facing = dir
        npcSpriteSheet = pygame.image.load('images/npc_sheet.png').convert() # Load player's spritesheet
        self.npcSprite = spriteSheet.SpriteSheet(npcSpriteSheet)
        self.image = self.npcSprite.getImage(self.facing*4,36,41,const.scale)
        self.rect = self.image.get_rect(center = self.pos)
        self.pos = Vector2(self.rect.center)

    def turn(self, faceDir):
        self.facing = faceDir
        self.image = self.npcSprite.getImage(self.facing*4,36,41,const.scale)

    def turnBack(self):
        self.turn(self.baseDir)

    def updatePos(self, screenMove):
        self.setPos((self.rect[0] + screenMove[0]/2 + 18, self.rect[1] + screenMove[1]/2 + 20))

    def setPos(self, pos):
        self.pos = pos
        self.rect.center = self.pos
        self.resetRect()

    def resetRect(self):
        self.rect.height = 35
        self.pos = Vector2(self.rect.center)
        
    # Draw the npc on the screen
    def draw(self, screen):
        drawRect = self.rect.copy()
        drawRect.y -= 12
        screen.blit(self.image, drawRect)