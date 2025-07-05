import pygame
import const
import tile
import item
import random

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
        self.items = []
        # Blit all the tiles to a single background image
        for i,row in enumerate(self.layout):
            for j,oneTile in enumerate(row):
                self.background.blit(oneTile.image, (i*const.tileSize, j*const.tileSize))
        self.updatePos(pos)

    def updatePos(self, screenCenter):
        self.pos = screenCenter
        self.rect = self.background.get_rect(center = self.pos)
        halfLength = round((len(self.layout)-1)/2)
        self.solidRects: list[pygame.Rect] = []
        self.items: list[item.Item] = []
        for i, row in enumerate(self.layout):
            for j, tile in enumerate(row):
                tilePos = (screenCenter[0]-(i-halfLength)*const.tileSize,screenCenter[1]-(j-halfLength)*const.tileSize)
                tile.updatePos(tilePos)
                if tile.solid:
                    newRect = pygame.Rect(i*const.tileSize, j*const.tileSize, const.tileSize, const.tileSize)
                    newRect.center = tilePos
                    self.solidRects.append(newRect)
                elif tile.tileType == 5: # Tile has a crate on it
                    newRect = pygame.Rect(i*const.tileSize, j*const.tileSize, const.tileSize*0.6, const.tileSize*0.6)
                    newRect.topleft = (tilePos[0]-4, tilePos[1]-4)
                    self.solidRects.append(newRect)
                if tile.item:
                    self.items.append(tile.item)

    def removeItem(self, item: item.Item):
        self.items.remove(item)
        for row in self.layout:
            for tile in row:
                if tile.item == item:
                    tile.deleteItem()


    # Draw each tile in this room
    def draw(self, screen):
        screen.blit(self.background, self.rect)
        for item in self.items:
            item.draw(screen)
    
    # Construct the room tiles from the given layout
    # Only use once upon creation
    def initialize(self, layout):
        # Create the correct tile by the number
        for i,row in enumerate(layout):
            self.layout.append([])
            for j,c in enumerate(row):
                if c == 0: # Wall
                    self.layout[i].append(tile.Tile(6, (0,0), const.scale))
                elif c == 1: # Floor
                    self.layout[i].append(tile.Tile(random.randint(1,3), (0,0), const.scale))
                elif c == 2: # Shelf
                    self.layout[i].append(tile.Tile(random.randint(7,15), (0,0), const.scale))
                elif c == 3: # Exit
                    self.exit = tile.Tile(0, (0,0), const.scale)
                    self.layout[i].append(self.exit)
                elif c == 4: # crate
                    self.layout[i].append(tile.Tile(5, (0,0), const.scale))
                elif c == 9: # Lift floor
                    self.layout[i].append(tile.Tile(4, (0,0), const.scale))
                elif c == 8: # Lift wall
                    self.layout[i].append(tile.Tile(16, (0,0), const.scale))
        # Set the neighbours for the tiles
        for i, row in enumerate(self.layout):
            for j, c in enumerate(row):
                if j: # Set the tile on top as neighbour if this isn't the top tile
                    self.layout[i][j-1].setNeighbour(0,c)
                if i: # Set the previous tile as neighbour if this isn't the first tile
                    self.layout[i-1][j].setNeighbour(1,c)
        # Correct Shelf orientation
        '''
        for i, row in enumerate(self.layout):
            for j, c in enumerate(row):
                if c.isShelf(): # Tile is a shelf
                    if c.neighbours[0] and c.neighbours[0].isShelf() and c.neighbours[1] and c.neighbours[1].isShelf():
                        c.changeType(9)
                        c.rotateImage()
                    elif c.neighbours[1] and c.neighbours[1].isShelf() and c.neighbours[2] and c.neighbours[2].isShelf():
                        c.changeType(9)
                        c.rotateImage(2)
                    elif c.neighbours[2] and c.neighbours[2].isShelf() and c.neighbours[3] and c.neighbours[3].isShelf():
                        c.changeType(9)
                        c.rotateImage(3)
                    elif c.neighbours[3] and c.neighbours[3].isShelf() and c.neighbours[0] and c.neighbours[0].isShelf():
                        c.changeType(9)
                    elif (c.neighbours[0] and c.neighbours[0].isShelf()) or (c.neighbours[2] and c.neighbours[2].isShelf()):
                        c.rotateImage()
        '''
