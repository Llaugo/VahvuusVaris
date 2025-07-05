import pygame
import spriteSheet
import const
import item
import random



class Tile():
    # tileType: The number tells what kind of tile this is and what image to use for it
    # pos: A double for the x and y coordinates of the tile center
    # scale: For determining the image size
    def __init__(self, tileType, pos, scale):
        tileSpriteSheet = pygame.image.load('images/shopsprite.png').convert() # Load tile spritesheet
        self.tileSprite = spriteSheet.SpriteSheet(tileSpriteSheet)
        self.tileType = tileType
        self.scale = scale
        self.pos = pos
        self.itemCorner = (random.randint(0,1)*2-1, random.randint(0,1)*2-1) # helps to figure out and randomize item location on the tile
        self.image = self.tileSprite.getImage(tileType, const.tileSize, const.tileSize, self.scale)
        self.rect = self.image.get_rect(center = pos)
        self.solid = True # Can the tile be walked on
        self.item = None
        if tileType < 6: self.solid = False # The first six tiles are not solid and can be walked on
        self.neighbours = [None, None, None, None] # Down, Right, Up, Left
        if self.isShelf() and const.itemProbability > random.random():
            self.item = item.Item(self.itemPos())
        # self.playerOccupied = False

    # Method for setting another tile as a neighbour for this one
    # dir: direction where a neighbouring tile is set. 0,1,2,3 = d,r,u,l
    # tile: another tile object
    def setNeighbour(self, dir, tile):
        if self.neighbours[dir] != None or tile.neighbours[(dir + 2) % 4] != None: # Check if neighbour exists
            raise ValueError('Tried to set neighbour for a tile that already has that neighbour set.')
        self.neighbours[dir] = tile # Set the other tile as a neighbour for this tile.
        tile.neighbours[(dir + 2) % 4] = self # Set this tile as a neighbour for the other tile. (in the opposite direction)

    '''
    # Rotate the image of the tile
    # count: how many times counterclockwise
    def rotateImage(self, count = 1):
        self.image = pygame.transform.rotate(self.image, 90*count)
        self.rect = self.image.get_rect(center = self.pos)
        self.rotated = (self.rotated + count) % 4
        if self.item:
            self.item.updatePos(self.itemPos())
    

    # tileType: new tile type and changes the image
    def changeType(self, tileType):
        self.tileType = tileType
        self.image = self.tileSprite.getImage(tileType, const.tileSize, const.tileSize, self.scale)
    '''
    
    def isShelf(self):
        if self.tileType >= 7 and self.tileType <= 15:
            return True
        else:
            return False

    def updatePos(self, pos):
        self.pos = pos
        self.rect.center = pos
        if self.item:
            self.item.updatePos(self.itemPos())

    def itemPos(self):
        return (self.pos[0] + 8*self.itemCorner[0], self.pos[1] + 8*self.itemCorner[1])
        '''
        if self.tileType == 9:
            if self.rotated % 2 == 0:
                return (self.pos[0] + 8*(self.rotated-1), self.pos[1] - 8*(self.rotated-1))
            else:
                return (self.pos[0] + 8*(self.rotated-2), self.pos[1] + 8*(self.rotated-2))
        else:
            return (self.pos[0] + (self.rotated%2)*(self.rotated-2)*8, self.pos[1] + ((self.rotated+1)%2)*(self.rotated-1)*8)
        '''

    # Deletes a possible held item and returns it
    def deleteItem(self):
        deletedItem = self.item
        self.item = None
        return deletedItem