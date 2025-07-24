import pygame
import spriteSheet
import const
import item
import advert
import random


# Class for different tiles in the rooms
class Tile():
    # tileType: The number tells what kind of tile this is and what image to use for it
    # pos: A double for the x and y coordinates of the tile center
    # scale: For determining the image size
    # roomDistance: How far away the room/item is from the middle. Far away rooms produce more rarer items.
    def __init__(self, tileType, roomDistance=0):
        tileSpriteSheet = pygame.image.load('images/shopsprite.png').convert() # Load tile spritesheet
        self.tileSprite = spriteSheet.SpriteSheet(tileSpriteSheet)
        self.tileType = tileType
        self.pos = (0,0)
        self.scale = const.scale
        self.itemCorner = (random.randint(0,1)*2-1, random.randint(0,1)*2-1) # helps to figure out and randomize item location on the tile
        self.image = self.tileSprite.getImage(tileType, const.tileSize, const.tileSize, self.scale)
        self.rect = self.image.get_rect(center = self.pos)
        self.solid = True # Can the tile be walked on
        self.item = None # A possible item the tile holds
        self.advert = None
        if tileType < 7: self.solid = False # The first six tile types are not solid and can be walked on
        self.neighbours = [None, None, None, None] # Down, Right, Up, Left
        if self.isShelf() and const.itemProbability > random.random(): # Randomize if a shelf tile has an item or not
            self.item = item.Item(self.itemPos(), roomDistance)


    # Method for setting another tile as a neighbour for this one
    # dir: direction where a neighbouring tile is set. 0,1,2,3 = d,r,u,l
    # tile: another tile object
    def setNeighbour(self, dir, tile):
        if self.neighbours[dir] != None or tile.neighbours[(dir + 2) % 4] != None: # Check if neighbour exists
            raise ValueError('Tried to set neighbour for a tile that already has that neighbour set.')
        self.neighbours[dir] = tile # Set the other tile as a neighbour for this tile.
        tile.neighbours[(dir + 2) % 4] = self # Set this tile as a neighbour for the other tile. (in the opposite direction)

    # Make this tile a wall
    def makeWall(self):
        self.tileType = 7
        self.solid = True
        self.image = self.tileSprite.getImage(self.tileType, const.tileSize, const.tileSize, self.scale)
        
    # Make this tile a floor if it is water
    def clearWater(self):
        if self.isWater():
            self.tileType = 1
            self.solid = False
            self.image = self.tileSprite.getImage(self.tileType, const.tileSize, const.tileSize, self.scale)

    # Returns True if this tile is a shelf tile and False otherwise
    def isShelf(self):
        if self.tileType >= 8 and self.tileType <= 16:
            return True
        else:
            return False
        
    def isWater(self):
        if self.tileType == 18:
            return True
        else:
            return False
        
    def isAdvert(self):
        if self.tileType == 6:
            return True
        else:
            return False

    # Update pos of the tile
    def updatePos(self, pos):
        self.pos = pos
        self.rect.center = pos
        if self.item: # Update item pos
            self.item.updatePos(self.itemPos())
        if self.advert:
            self.advert.updatePos((self.pos[0]+8,self.pos[1]+1))

    # Get the item's location on the tile
    def itemPos(self):
        return (self.pos[0] + 8*self.itemCorner[0], self.pos[1] + 8*self.itemCorner[1])

    # Deletes a possible held item and returns it
    def deleteItem(self):
        deletedItem = self.item
        self.item = None
        return deletedItem
    
    # Adds an item to this tile if it is a shelf and the item isn't set already
    def addItem(self, roomDistance):
        if self.isShelf() and not self.item:
            self.item = item.Item(self.itemPos(), roomDistance)

    # Sets the advert of this tile if the tile is appropriate and advert is not set already
    def setAdvert(self, dir):
        if self.isAdvert() and not self.advert:
            self.advert = advert.Advert(dir)