import pygame
import spriteSheet
import const


class Tile():
    # tileType: The number tells what kind of tile this is and what image to use in the shop_sheet.png
    # pos: A double for the x and y coordinates of the tile center
    # scale: For determining the image size
    def __init__(self, tileType, pos, scale):
        tileSpriteSheet = pygame.image.load('images/shop_sheet2.png').convert() # Load tile spritesheet
        self.tileSprite = spriteSheet.SpriteSheet(tileSpriteSheet)
        self.tileType = tileType
        self.scale = scale
        self.pos = pos
        self.image = self.tileSprite.getImage(tileType, const.tileSize, const.tileSize, self.scale)
        self.rect = self.image.get_rect(center = pos)
        self.solid = True # Can the tile be walked on
        if tileType < 5: self.solid = False # The first five tiles are not solid and can be walked on
        self.neighbours = [None, None, None, None] # Down, Right, Up, Left
        # self.playerOccupied = False

    # Method for setting another tile as a neighbour for this one
    # dir: direction where a neighbouring tile is set. 0,1,2,3 = d,r,u,l
    # tile: another tile object
    def setNeighbour(self, dir, tile):
        if self.neighbours[dir] != None or tile.neighbours[(dir + 2) % 4] != None: # Check if neighbour exists
            raise ValueError('Tried to set neighbour for a tile that already has that neighbour set.')
        self.neighbours[dir] = tile # Set the other tile as a neighbour for this tile.
        tile.neighbours[(dir + 2) % 4] = self # Set this tile as a neighbour for the other tile. (in the opposite direction)

    # Rotate the image of the tile
    # count: how many times counterclockwise
    def rotateImage(self, count = 1):
        self.image = pygame.transform.rotate(self.image, 90*count)
        self.rect = self.image.get_rect(center = self.pos)


    # tileType: new tile type
    def changeType(self, tileType):
        self.tileType = tileType
        self.image = self.tileSprite.getImage(tileType, const.tileSize, const.tileSize, self.scale)

    def isShelf(self):
        if self.tileType >= 6 and self.tileType <= 9:
            return True
        else:
            return False

    # Draws this tile on the screen
    def draw(self, screen):
        screen.blit(self.image, (self.rect))