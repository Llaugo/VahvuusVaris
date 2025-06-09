from sys import exit
import asyncio # For creating a browser view with pygbag
import pygame
import const
import spriteSheet
import playerClass
import button
import tile
import room
import random
import math




pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((const.worldWidth,const.worldHeight)) # Set screen size

# Initialize buttons for moving
downButton = button.Button(0,(const.worldWidth-115*const.scale,const.worldHeight-69*const.scale),const.scale)
rightButton = button.Button(2,(const.worldWidth-69*const.scale,const.worldHeight-115*const.scale),const.scale)
upButton = button.Button(4,(const.worldWidth-115*const.scale,const.worldHeight-161*const.scale),const.scale)
leftButton = button.Button(6,(const.worldWidth-161*const.scale,const.worldHeight-115*const.scale),const.scale)
buttons = [downButton, rightButton, upButton, leftButton]
# Finger and mouse positions are tracked in this dictionary (and can be compared with button locations)
buttonsPressed = {} 

# Player initialization
player = playerClass.Player(buttons)

room1 = room.Room(const.roomLayouts)

# Placeholder background
backg = (100,100,100)

async def main():

    # If active, shows useful information about the game. (For debug purposes)
    debugMode = False
    
    # Main game loop
    while True:
        # Event handler
        for event in pygame.event.get():
            # Quitting the game and closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Observe finger touches and track their location
            if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERMOTION:
                x = round(event.x * const.worldWidth)
                y = round(event.y * const.worldHeight)
                buttonsPressed[event.finger_id] = (x,y)
            elif event.type == pygame.FINGERUP: # Delete finger_id, if finger is lifted off
                buttonsPressed.pop(event.finger_id)
            # Observe mouse location when pressed
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                buttonsPressed["mousePress"] = pos
            #elif event.type == pygame.MOUSEBUTTONUP: # Stop mouse position tracking if mouse is lifted
            #    buttonsPressed.pop("mousePress")

        # Toggle debug mode
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            debugMode = not debugMode 

        # Check if any buttons are pressed
        for b in buttons:
            b.unpress()
            for pos in buttonsPressed.values():
                if b.rect.collidepoint(pos):
                    b.press()

        # Draw images to screen
        screen.fill(backg)                  # BG
        room1.draw(screen)                  # Room/tiles
        player.draw(screen)                 # player
        player.update(room1)                # player actions
        for b in buttons: b.draw(screen)    # buttons

        # Debug screen info
        if debugMode:
            debugfont = pygame.font.SysFont("fontname", 30)
            debug_surf = debugfont.render(f'Detected fingers: {buttonsPressed}',False,(50,50,50))
            debug_rect = debug_surf.get_rect(topleft = (10,10))
            screen.blit(debug_surf,debug_rect)

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
        

asyncio.run(main())