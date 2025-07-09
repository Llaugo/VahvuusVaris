import pygame
import const
import tile
import item
import random

# A class for rooms which consist of tiles in a grid.
class Room():
    # layout: the tile layout in the room
    # pos: position of the room
    def __init__(self, layout, pos):
        self.layout: list[list[tile.Tile]] = [] # Matrix of every tile
        self.pos = pos                          # Room center
        self.exit = None                        # Does the room have an exit
        self.initialize(layout)                 # Initialize room's tiles
        self.tiles = [x for xs in self.layout for x in xs] # All the room's tiles in a list
        self.background = pygame.Surface((len(layout[0]*const.tileSize), len(layout*const.tileSize))).convert() # Room background surface
        self.rect = self.background.get_rect(center = pos)
        self.solidRects = []                    # walls and solid objects of the room
        self.items = []                         # items in the room
        self.stones = []                        # stones in the room (list[(image,rect)])
        for i,row in enumerate(self.layout):    # Blit all the tiles to a single background image
            for j,oneTile in enumerate(row):
                self.background.blit(oneTile.image, (i*const.tileSize, j*const.tileSize))
        self.updatePos(pos)                     # Set positions correctly

    # Update room position
    # screenCenter: center of the screen
    def updatePos(self, screenCenter):
        self.pos = screenCenter
        self.rect = self.background.get_rect(center = self.pos)
        halfLength = round((len(self.layout)-1)/2)  # Helper value
        self.solidRects: list[pygame.Rect] = []     # Reset solids
        self.items: list[item.Item] = []            # Reset items
        for i, row in enumerate(self.layout):       # Update all tile positions
            for j, tile in enumerate(row):
                tilePos = (screenCenter[0]-(i-halfLength)*const.tileSize,screenCenter[1]-(j-halfLength)*const.tileSize)
                tile.updatePos(tilePos)             # Update tile
                if tile.solid:                      # Update solid walls
                    newRect = pygame.Rect(i*const.tileSize, j*const.tileSize, const.tileSize, const.tileSize)
                    newRect.center = tilePos
                    self.solidRects.append(newRect)
                elif tile.tileType == 5:            # Update crate tiles
                    newRect = pygame.Rect(i*const.tileSize, j*const.tileSize, 23, 25)
                    newRect.center = (tilePos[0]+5, tilePos[1]+5)
                    self.solidRects.append(newRect)
                if tile.item:                       # Update items
                    self.items.append(tile.item)

    # Remove item from the rooms memory
    # item: the item to be removed
    def removeItem(self, item: item.Item):
        self.items.remove(item)         # Remove from the room
        for row in self.layout:
            for tile in row:
                if tile.item == item:   # And remove from the tile's memory
                    tile.deleteItem()

    # Add a stone to the room
    def addStone(self, pos):
        image = pygame.image.load('images/stone.png').convert_alpha() # Get image
        rect = image.get_rect(center = pos) # Get rect
        self.stones.append((image, rect))


    # Draw each tile, item and stone in this room
    def draw(self, screen):
        screen.blit(self.background, self.rect) # background
        for item in self.items:                 # items
            item.draw(screen)
        for stn in self.stones:                 # stones
            screen.blit(stn[0],stn[1])
    
    # Construct the room tiles from the given layout
    # Only use once upon creation
    # layout: the number matrix of the room's layout
    def initialize(self, layout):
        lift = (len(layout) <= 5) # The layout represents a lift
        # Create the correct tile by the number
        for i,row in enumerate(layout):
            self.layout.append([])
            for j,c in enumerate(row):
                if c == 0: # Wall
                    if lift: # Lift has special walls
                        self.layout[i].append(tile.Tile(16, (0,0), const.scale))
                    else:
                        self.layout[i].append(tile.Tile(6, (0,0), const.scale))
                elif c == 1: # Floor
                    if lift: # Lift has special floor
                        self.layout[i].append(tile.Tile(4, (0,0), const.scale))
                    else:
                        self.layout[i].append(tile.Tile(random.randint(1,3), (0,0), const.scale))
                elif c == 2: # Shelf
                    self.layout[i].append(tile.Tile(random.randint(7,15), (0,0), const.scale))
                elif c == 3: # Exit
                    self.exit = tile.Tile(0, (0,0), const.scale)
                    self.layout[i].append(self.exit)
                elif c == 4: # crate
                    self.layout[i].append(tile.Tile(5, (0,0), const.scale))
                else:
                    raise ValueError('The room layout contains unknown values')
        # Set the neighbours for the tiles
        for i, row in enumerate(self.layout):
            for j, c in enumerate(row):
                if j: # Set the tile on top as neighbour if this isn't the top tile
                    self.layout[i][j-1].setNeighbour(0,c)
                if i: # Set the previous tile as neighbour if this isn't the first tile
                    self.layout[i-1][j].setNeighbour(1,c)
