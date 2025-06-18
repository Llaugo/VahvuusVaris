import pygame
import const
import tile
from random import randint

# A class for rooms which consist of tiles in a grid.
class Room():
    def __init__(self, layout, pos):
        self.layout: list[list[tile.Tile]] = []
        self.exit = None
        self.initialize(layout) # Initialize room's tiles
        self.updatePos(pos)
        self.tiles = [x for xs in self.layout for x in xs] # All the room's tiles in a list

    def updatePos(self, screenCenter):
        halfLength = round((len(self.layout)-1)/2)
        i = 0
        j = 0
        for row in self.layout:
            for tile in row:
                tile.rect = tile.image.get_rect(center = (screenCenter[0]-(i-halfLength)*46,screenCenter[1]-(j-halfLength)*46))
                j += 1
            i += 1
            j = 0

    # Draw each tile in this room
    def draw(self, screen):
        for tile in self.tiles:
            tile.draw(screen)
    
    # Construct the room tiles from the given layout
    # Only use once upon creation
    def initialize(self, layout):
        i = 0
        j = 0
        for row in layout:
            self.layout.append([])
            for c in row:
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
                j += 1
            i += 1
            j = 0
        # Set the neighbours for the tiles
        for row in self.layout:
            i = 0
            for c in row:
                j = 0
                if j: # Set the tile on top as neighbour if this isn't the top tile
                    self.layout[i][j-1].setNeighbour(0,c)
                if i: # Set the previous tile as neighbour if this isn't the first tile
                    self.layout[i-1][j].setNeighbour(1,c)
                j += 1
            i += 1