import pygame
import spriteSheet


class Tile():
    # tileType: The number tells what kind of tile this is and what image to use in the shop_sheet.png
    # pos: A double for the x and y coordinates of the tile center
    # scale: For determining the image size
    def __init__(self, tileType, pos, scale):
        tileSpriteSheet = pygame.image.load('images/shop_sheet.png').convert() # Load tile spritesheet
        self.tileSprite = spriteSheet.SpriteSheet(tileSpriteSheet)
        self.tileType = tileType
        self.image = self.tileSprite.getImage(tileType,46,46,scale)
        self.rect = self.image.get_rect(center = pos)
        self.solid = True
        if tileType < 4: self.solid = False # The first four tiles are not solid and can be walked on

    def draw(self, screen):
        screen.blit(self.image, (self.rect))