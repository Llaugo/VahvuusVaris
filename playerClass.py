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
    # pos: player location on the screen
    def __init__(self, controls: tuple[button.Button,button.Button,button.Button,button.Button], pos):
        super().__init__()
        self.scale = const.scale # Scale of the player image
        self.playerSpeed = const.basePlayerSpeed
        self.speedDuration = 0 # Duration of a possible speed boost
        playerSpriteSheet = pygame.image.load('images/player_sheet.png').convert() # Load player's spritesheet
        self.playerSprite = spriteSheet.SpriteSheet(playerSpriteSheet)
        self.image = self.playerSprite.getImage(0,36,41,self.scale)
        self.facing = 0 # 0,1,2,3 = down,right,up,left
        self.walking = 0 # When rounded 0 = standing, 1,2,3 = walking (Animation helper)
        self.resetRect(pos) # Set player pos
        self.controls = controls

        
    # Tracks for each movement key/button if they are pressed and updates the direction the
    # player is facing and moves the walking animation value up.
    # room: The room the player is in
    def player_input(self, room: room.Room):
        keys = pygame.key.get_pressed()
        moving = True
        if keys[pygame.K_s] or self.controls[0].activeFinger: # Down key or button
            self.facing = 0
            self.walking = (self.walking + self.playerSpeed/20.0) % 4
        elif keys[pygame.K_d] or self.controls[1].activeFinger: # Right key or button
            self.facing = 1
            self.walking = (self.walking + self.playerSpeed/20.0) % 4
        elif keys[pygame.K_w] or self.controls[2].activeFinger: # Up key or button
            self.facing = 2
            self.walking = (self.walking + self.playerSpeed/20.0) % 4
        elif keys[pygame.K_a] or self.controls[3].activeFinger: # Left key or button
            self.facing = 3
            self.walking = (self.walking + self.playerSpeed/20.0) % 4
        else: # If no buttons are pressed, we want the first picture of the animation (standing)
            self.walking = 0
            moving = False
        if moving: # If some movement button was pressed move the player that direction
            if self.facing == 0:                               
                self.rect.y += self.playerSpeed 
            elif self.facing == 1:
                self.rect.x += self.playerSpeed
            elif self.facing == 2:
                self.rect.y -= self.playerSpeed
            else:
                self.rect.x -= self.playerSpeed
            self.resolveCollision(room) # Resolve collisions with walls etc.
        animationFrame = self.facing*4 + round(self.walking) % 4 # Get the correct image (frame of the animation)
        self.image = self.playerSprite.getImage(animationFrame,36,41,self.scale)
        
    # Handle player collision with a wall in a room
    def resolveCollision(self, room: room.Room):
        for solid in room.solidRects:                       # Check all the solid rects in the room
            if self.rect.colliderect(solid):
                overlap = self.rect.clip(solid)             # Compute overlap rectangle
                if overlap.width < overlap.height:          # Choose the smaller overlap dimension
                    if self.rect.centerx > solid.centerx:   # Player is on right side of tile -> push right
                        self.rect.left = solid.right 
                    else:
                        self.rect.right = solid.left        # Player is on left side -> push left
                else:
                    if self.rect.centery > solid.centery:   # Player is below tile -> push down
                        self.rect.top = solid.bottom
                    else:
                        self.rect.bottom = solid.top        # Player is above tile -> push up

    # Update player's state in the room
    def update(self, room):
        self.player_input(room) # Take input
        self.speedDuration = max(self.speedDuration-1, 0) # update speedboost timer
        if not self.speedDuration: # Reset speed when timer runs out
            self.resetSpeed()

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

    # Toggle the player size
    # room: room the player is in
    # newScale: the scale with respect to the original player size
    def toggleSize(self, room, newScale=1):
        if self.scale == const.scale:           # If the scale is normal
            self.scale = const.scale*newScale   # Change scale to new scale
            self.updatePos((0,0))
        else:
            self.scale = const.scale            # Set scale back to normal
            self.updatePos((0,0))
        self.resolveCollision(room)             # Resolve any collitions from changing the size

    # Change player speed
    def changeSpeed(self, speed, duration):
        if duration > self.speedDuration: # If new speedChange is longer than current, change speed
            self.playerSpeed = speed
            self.speedDuration = duration

    # Reset player speed to normal
    def resetSpeed(self):
        self.playerSpeed = const.basePlayerSpeed
        self.speedDuration = 0

    # Draw the player
    def draw(self, screen):
        drawRect = self.rect.copy()
        drawRect.y -= 20*self.scale # Adjust hitbox position to center on the image
        drawRect.x -= 5*self.scale
        screen.blit(self.image, drawRect)