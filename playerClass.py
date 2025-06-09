import pygame
import const
import spriteSheet
import button
import tile
import room
import math

# Player class tracking movement and walking animations.
class Player(pygame.sprite.Sprite):
    # controls: Consists of four control buttons (d,r,u,l) of the Button class
    def __init__(self, controls: tuple[button.Button,button.Button,button.Button,button.Button]):
        super().__init__()
        playerSpriteSheet = pygame.image.load('images/player_sheet_ph.png').convert() # Load player's spritesheet
        self.playerSprite = spriteSheet.SpriteSheet(playerSpriteSheet)
        self.image = self.playerSprite.getImage(0,32,46,const.scale)
        self.facing = 0 # 0,1,2,3 = down,right,up,left
        self.walking = 0 # When rounded 0 = standing, 1,2,3 = walking
        self.rect = self.image.get_rect(midbottom = (const.worldWidth/2, const.worldHeight/2))
        self.rect = pygame.Rect.inflate(self.rect, 0, -5)
        print(self.rect)
        self.controls = controls
        
    # Tracks for each movement key/button if they are pressed and updates the direction the
    # player is facing and moves the walking animation value up.
    # room: The room the player is in
    def player_input(self, room: room.Room):
        keys = pygame.key.get_pressed()
        moving = True
        if keys[pygame.K_DOWN] or self.controls[0].activated: # Down key or button
            self.facing = 0
            self.walking = (self.walking + const.playerSpeed/20.0) % 4
        elif keys[pygame.K_RIGHT] or self.controls[1].activated: # Right key or button
            self.facing = 1
            self.walking = (self.walking + const.playerSpeed/20.0) % 4
        elif keys[pygame.K_UP] or self.controls[2].activated: # Up key or button
            self.facing = 2
            self.walking = (self.walking + const.playerSpeed/20.0) % 4
        elif keys[pygame.K_LEFT] or self.controls[3].activated: # Left key or button
            self.facing = 3
            self.walking = (self.walking + const.playerSpeed/20.0) % 4
        else: # If no buttons are pressed, we want the first picture of the animation (standing)
            self.walking = 0
            moving = False
        if moving:
            self.move(self.facing, room)
        animationFrame = self.facing*4 + round(self.walking) % 4
        self.image = self.playerSprite.getImage(animationFrame,32,46,const.scale)

    # Check if player collides with a certain tile
    def collidesWithTile(self, tile: tile.Tile):
        doesCollide = False
        if self.rect.colliderect(tile.rect) and tile.solid: 
            doesCollide = True
        return doesCollide
    # Check if player collides with any tile in a certain room
    def collidesWithRoom(self, room: room.Room):
        for tile in room.tiles():
            if self.collidesWithTile(tile):
                return True
        return False

    # Moves the player a direction, if there isn't anything in the way
    def move(self, dir, room: room.Room):
        if dir == 0:                                # For a given direction,
            self.rect.y += const.playerSpeed        # move the player that direction.
            if self.collidesWithRoom(room):             # If there's something in the way,
                self.rect.y -= const.playerSpeed    # move the player back.
        elif dir == 1:
            self.rect.x += const.playerSpeed
            if self.collidesWithRoom(room):
                self.rect.x -= const.playerSpeed
        elif dir == 2:
            self.rect.y -= const.playerSpeed
            if self.collidesWithRoom(room):
                self.rect.y += const.playerSpeed
        else:
            self.rect.x -= const.playerSpeed
            if self.collidesWithRoom(room):
                self.rect.x += const.playerSpeed

    def update(self, room):
        self.player_input(room)

    def draw(self, screen):
        draw_rect = self.rect.copy()         # 1) copy the logical rect
        draw_rect.y -= 5         # 2) move it up by however many pixels you need
        screen.blit(self.image, draw_rect)