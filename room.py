import pygame
import const
import tile
from random import randint

# A class for rooms which consist of tiles in a grid.
class Room():
    def __init__(self, layout, pos):
        self.layout: list[list[tile.Tile]] = []
        self.pos = pos
        self.exit = None
        self.initialize(layout) # Initialize room's tiles
        self.tiles = [x for xs in self.layout for x in xs] # All the room's tiles in a list
        self.background = pygame.Surface((len(layout[0]*const.tileSize), len(layout*const.tileSize))).convert()
        self.rect = self.background.get_rect(center = pos)
        self.solidRects = []
        for i,row in enumerate(self.layout):
            for j,oneTile in enumerate(row):
                self.background.blit(oneTile.image, (i*const.tileSize, j*const.tileSize))
                if oneTile.solid:
                    self.solidRects.append(pygame.Rect(0, 0, const.tileSize, const.tileSize))
        self.updatePos(pos)

    def updatePos(self, screenCenter):
        self.pos = screenCenter
        self.rect = self.background.get_rect(center = self.pos)
        halfLength = round((len(self.layout)-1)/2)
        self.solidRects = []
        for i, row in enumerate(self.layout):
            for j, tile in enumerate(row):
                tile.rect = tile.image.get_rect(center = (screenCenter[0]-(i-halfLength)*const.tileSize,screenCenter[1]-(j-halfLength)*const.tileSize))
                if tile.solid:
                    newRect = pygame.Rect(i*const.tileSize, j*const.tileSize, const.tileSize, const.tileSize)
                    newRect.center = (screenCenter[0]-(i-halfLength)*const.tileSize,screenCenter[1]-(j-halfLength)*const.tileSize)
                    self.solidRects.append(newRect)

    # Draw each tile in this room
    def draw(self, screen):
        screen.blit(self.background, self.rect)
    
    # Construct the room tiles from the given layout
    # Only use once upon creation
    def initialize(self, layout):
        for i,row in enumerate(layout):
            self.layout.append([])
            for j,c in enumerate(row):
                if c == 0: # Wall
                    self.layout[i].append(tile.Tile(5, (0,0), const.scale))
                elif c == 1: # Floor
                    self.layout[i].append(tile.Tile(randint(1,3), (0,0), const.scale))
                elif c == 2: # Shelf
                    self.layout[i].append(tile.Tile(randint(6,8), (0,0), const.scale))
                elif c == 3: # Exit
                    self.exit = tile.Tile(0, (0,0), const.scale)
                    self.layout[i].append(self.exit)
                elif c == 9: # Lift floor
                    self.layout[i].append(tile.Tile(4, (0,0), const.scale))
                elif c == 8: # Lift wall
                    self.layout[i].append(tile.Tile(9, (0,0), const.scale))
                    
        # Set the neighbours for the tiles
        #i = 0
        #j = 0
        #for row in self.layout:
        #    for c in row:
        #        j = 0
        #        if j: # Set the tile on top as neighbour if this isn't the top tile
        #            self.layout[i][j-1].setNeighbour(0,c)
        #        if i: # Set the previous tile as neighbour if this isn't the first tile
        #            self.layout[i-1][j].setNeighbour(1,c)
        #        j += 1
        #    i += 1