from sys import exit
import asyncio # For creating a browser view with pygbag
import pygame
import const
import spriteSheet
import playerClass
import button
import tile
import room
import picture
import random
import math




pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((const.worldWidth,const.worldHeight), pygame.RESIZABLE) # Set screen size


# Initialize buttons for moving
downButton = button.Button(0,(const.worldWidth-115*const.scale,const.worldHeight-69*const.scale),const.scale)
rightButton = button.Button(2,(const.worldWidth-69*const.scale,const.worldHeight-115*const.scale),const.scale)
upButton = button.Button(4,(const.worldWidth-115*const.scale,const.worldHeight-161*const.scale),const.scale)
leftButton = button.Button(6,(const.worldWidth-161*const.scale,const.worldHeight-115*const.scale),const.scale)
moveButtons = [downButton, rightButton, upButton, leftButton]
exitButton = button.Button(8,(const.worldWidth-231*const.scale,const.worldHeight-115*const.scale),const.scale)
# Finger and mouse positions are tracked in this dictionary (and can be compared with button locations)
fingerPositions = {} 

frame = picture.Picture("images/frame.png", (710,710), (const.worldWidth/2,const.worldHeight/2))

# Player initialization
player = playerClass.Player(moveButtons, (const.worldWidth/2*const.scale,const.worldHeight/2*const.scale))
room1 = room.Room(const.roomLayouts)

# gameStatus: Shows the state of the game
# "level": Game is running a level
# "menu": Game is at the starting menu
# "checkpoint": Game is at a state in between levels
gameStatus = "level"

# Placeholder background
backg = (160,209,255)

async def main():

    # If active, shows useful information about the game. (For debug purposes)
    debugMode = False
    screenSize = pygame.display.get_window_size()
    
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
                fingerPositions[event.finger_id] = (x,y)
            elif event.type == pygame.FINGERUP: # Delete finger_id, if finger is lifted off
                fingerPositions.pop(event.finger_id)
            # Observe mouse location when pressed
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                fingerPositions["mousePress"] = pos
            #elif event.type == pygame.MOUSEBUTTONUP: # Stop mouse position tracking if mouse is lifted
            #    fingerPositions.pop("mousePress")

        # Toggle debug mode
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            debugMode = not debugMode

        #########################################################
        # IN THE MAIN MENU
        #########################################################
        if gameStatus == "menu":
            pass


        #########################################################
        # RUNNING A LEVEL
        #########################################################
        if gameStatus == "level":

            # Check if any buttons are pressed
            for b in moveButtons:
                b.unpress()
                for pos in fingerPositions.values():
                    if b.rect.collidepoint(pos):
                        b.press()

            # Draw images to screen
            newScreenSize = pygame.display.get_window_size()
            # Update all positions if the screen size was changed
            if newScreenSize != screenSize:
                screenMove = (newScreenSize[0]-screenSize[0], newScreenSize[1]-screenSize[1])
                room1.updatePos((newScreenSize[0]/2,newScreenSize[1]/2))
                player.updatePos(screenMove)
                downButton.updatePos((newScreenSize[0]-115*const.scale,newScreenSize[1]-69*const.scale))
                rightButton.updatePos((newScreenSize[0]-69*const.scale,newScreenSize[1]-115*const.scale))
                upButton.updatePos((newScreenSize[0]-115*const.scale,newScreenSize[1]-161*const.scale))
                leftButton.updatePos((newScreenSize[0]-161*const.scale,newScreenSize[1]-115*const.scale))
                exitButton.updatePos((newScreenSize[0]-231*const.scale,newScreenSize[1]-115*const.scale))
                frame.updatePos((newScreenSize[0]/2,newScreenSize[1]/2))
            screen.fill(backg)                                          # BG
            room1.draw(screen)                                          # Room/tiles
            player.draw(screen)                                         # player
            player.update(room1)                                        # player actions
            for b in moveButtons:                                       # buttons
                b.draw(screen)                    
            frame.draw(screen)    
            if room1.exit != None and room1.exit.rect.colliderect(player.rect):
                exitButton.draw(screen)                                 # exit button, if player is at the lift
                exitButton.unpress()
                for pos in fingerPositions.values():
                    if exitButton.rect.collidepoint(pos):
                        exitButton.press()
            screenSize = newScreenSize

        #########################################################
        # CHECKPOINT IN BETWEEN LEVELS
        #########################################################
        if gameStatus == "checkpoint":
            pass

        # Debug screen info
        if debugMode:
            debugfont = pygame.font.SysFont("fontname", 30)
            debug_surf = debugfont.render(f'Detected fingers: {fingerPositions}',False,(50,50,50))
            debug_rect = debug_surf.get_rect(topleft = (10,10))
            screen.blit(debug_surf,debug_rect)

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
        

asyncio.run(main())