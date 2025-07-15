import pygame
import const
import spriteSheet
import button
import tile
import room
import math
from pygame.math import Vector2

# Player class tracking movement and walking animations.
class Player(pygame.sprite.Sprite):
    # controls: Consists of four control buttons (d,r,u,l) of the Button class
    # pos: player location on the screen
    def __init__(self, controls: tuple[button.Button,button.Button,button.Button,button.Button], pos):
        super().__init__()
        self.scale = const.scale # Scale of the player image
        self.playerSpeed = const.basePlayerSpeed
        self.speedDuration = 0 # Duration of a possible speed boost
        self.swimSpeed = 0     # Player's speed on water
        self.swimDuration = 0  # Duration of the swim speed
        playerSpriteSheet = pygame.image.load('images/player_sheet.png').convert() # Load player's spritesheet
        self.playerSprite = spriteSheet.SpriteSheet(playerSpriteSheet)
        self.image = self.playerSprite.getImage(0,36,41,self.scale)
        self.facing = 0 # 0,1,2,3 = down,right,up,left
        self.walking = 0 # When rounded 0 = standing, 1,2,3 = walking (Animation helper)
        self.resetRect(pos) # Set player pos
        self.pos = Vector2(self.rect.center)
        self.controls = controls

        
    # Tracks for each movement key/button if they are pressed and updates the direction the
    # player is facing and moves the walking animation value up.
    # room: The room the player is in
    def playerInput(self, room: room.Room):
        keys = pygame.key.get_pressed()
        velocity = Vector2()
        speed = self.playerSpeed*self.swimSpeed if self.isInWater(room) else self.playerSpeed
        if keys[pygame.K_s] or self.controls[0].activeFinger: # Down key or button
            self.facing = 0
            velocity += Vector2(0,1)
        elif keys[pygame.K_d] or self.controls[1].activeFinger: # Right key or button
            self.facing = 1
            velocity += Vector2(1,0)
        elif keys[pygame.K_w] or self.controls[2].activeFinger: # Up key or button
            self.facing = 2
            velocity += Vector2(0,-1)
        elif keys[pygame.K_a] or self.controls[3].activeFinger: # Left key or button
            self.facing = 3
            velocity += Vector2(-1,0)
        #if velocity.y:
        #    velocity.x = 0
        # self.facing = 1 - velocity.y ? 2 - velocity.x
        if not velocity: # If no buttons are pressed, we want the first picture of the animation (standing)
            self.walking = 0
        else:
            self.pos += (velocity*speed)
            self.walking = (self.walking + speed/20.0) % 4
            self.resolveCollision(room) # Resolve collisions with walls etc.
            self.rect.center = (self.pos.x, self.pos.y)
        animationFrame = self.facing*4 + round(self.walking) % 4 # Get the correct image (frame of the animation)
        self.image = self.playerSprite.getImage(animationFrame,36,41,self.scale)
        
    # Handle player collision with a wall in a room
    def resolveCollision(self, room: room.Room):
        self.rect.center = (self.pos.x, self.pos.y)
        solids = room.solidRects.copy()
        if not self.swimDuration:
            solids += room.waterRects
        for solid in solids:                                # Check all the solid rects in the room
            if self.rect.colliderect(solid):
                overlap = self.rect.clip(solid)             # Compute overlap rectangle
                if overlap.width < overlap.height:          # Choose the smaller overlap dimension
                    if self.rect.centerx > solid.centerx:   # Player is on right side of tile -> push right
                        self.pos.x = solid.right + math.ceil(self.rect.width/2)
                    else:
                        self.pos.x = solid.left - math.ceil(self.rect.width/2)
                else:
                    if self.rect.centery > solid.centery:   # Player is below tile -> push down
                        self.pos.y = solid.bottom + math.ceil(self.rect.height/2)
                    else:
                        self.pos.y = solid.top - math.ceil(self.rect.height/2)
                self.rect.center = (self.pos.x, self.pos.y)

    # Update player's state in the room
    def update(self, room):
        self.playerInput(room) # Take input
        self.speedDuration = max(self.speedDuration-1, 0) # update speedboost timer
        if not self.speedDuration: # Reset speed when timer runs out
            self.resetSpeed()
        if self.swimDuration == 1 and self.isInWater(room): # Keep timer at 1, if player is still in the water
            self.swimSpeed = const.basePlayerSpeed*0.1
        else:
            self.swimDuration = max(self.swimDuration-1, 0) # update swimming timer
        if not self.swimDuration:
            self.resetSwim()

    # Update the pos of the player
    # screenMove: how much the screen size (x,y) has been changed
    def updatePos(self, screenMove):
        self.resetRect((self.rect[0] + screenMove[0]/2 + 18*self.scale, self.rect[1] + screenMove[1]/2 + 20*self.scale))

    # Reset player to the center of the screen
    # screenSize: dimensions of the window
    def resetPos(self, screenSize):
        self.resetRect((screenSize[0]/2, screenSize[1]/2))
        self.facing = 0

    # Set a new position for the rect and make it smaller than the image
    def resetRect(self, pos):
        self.image = self.playerSprite.getImage(self.facing*4,36,41,self.scale)
        self.rect = self.image.get_rect(center = pos)
        self.rect.height -= 20*self.scale # Make the player rect slimmer
        self.rect.width -= 10*self.scale  # Make the player rect shorter
        self.pos = Vector2(self.rect.center)

    # Toggle the player size
    # room: room the player is in
    # newScale: the scale with respect to the original player size
    def toggleSize(self, room, newScale=1):
        if self.scale == const.scale:           # If the scale is normal
            self.scale = const.scale*newScale   # Change scale to new scale
            self.updatePos((10,0))
        else:
            self.scale = const.scale            # Set scale back to normal
            self.updatePos((-10,0))
        self.resolveCollision(room)             # Resolve any collitions from changing the size

    # Change player speed
    def changeSpeed(self, speed, duration):
        if duration > self.speedDuration: # If new speed duration is longer than current, change speed
            self.playerSpeed = speed
            self.speedDuration = duration

    # Reset player speed to normal
    def resetSpeed(self):
        self.playerSpeed = const.basePlayerSpeed
        self.speedDuration = 0

    # Change players swimming speed
    def swim(self, speed, duration):
        if duration > self.swimDuration:
            self.swimSpeed = speed
            self.swimDuration = duration

    # Reset player swimming speed
    def resetSwim(self):
        self.swimSpeed = 0
        self.swimDuration = 0
    
    # Returns true if player is colliding with water tiles in the given room
    def isInWater(self,room):
        for water in room.waterRects:
            if self.rect.colliderect(water):
                return True
        return False

    # Draw the player
    def draw(self, screen):
        drawRect = self.rect.copy()
        drawRect.y -= 20*self.scale # Adjust hitbox position to center on the image
        drawRect.x -= 5*self.scale
        screen.blit(self.image, drawRect)