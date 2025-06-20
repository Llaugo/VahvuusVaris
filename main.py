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
import text
import shoppingList
import random
import math
import time



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
nextFloorButton = button.Button(10,(const.worldWidth/2,const.worldHeight*3/4),const.scale)
# Finger and mouse positions are tracked in this dictionary (and can be compared with button locations)
fingerPositions = {} 


# Player initialization
player = playerClass.Player(moveButtons, (const.worldWidth/2*const.scale,const.worldHeight/2*const.scale))


# Different font sizes
xsGameFont = pygame.font.SysFont(None, 22)
sGameFont = pygame.font.SysFont(None, 30)
mGameFont = pygame.font.SysFont(None, 50)
lGameFont = pygame.font.SysFont(None, 80)


# Background color
backg = (160,209,255)

async def main():

    # If active, shows useful information about the game. (For debug purposes)
    debugMode = True
    screenSize = pygame.display.get_window_size()
    # gameStatus: Shows the state of the game
    # "level": Game is running a level
    # "menu": Game is at the starting menu
    # "checkpoint": Game is at a state in between levels
    gameStatus = "level"
    # Tracks the floor/level the player is at
    floorNumber = 1
    room1 = room.Room(const.roomLayouts[0],(screenSize[0]/2,screenSize[1]/2))
    lobby = room.Room(const.lobbyLayout, (screenSize[0]/2,screenSize[1]/2))

    frame = picture.Picture("images/frame.png", (710,710), (const.worldWidth/2, const.worldHeight/2))
    shoplist = picture.Picture("images/shoplist.png", (230,230), (const.worldWidth - room1.rect.left/2, const.worldHeight/4))
    shoplistTitle = text.Text(sGameFont,"Ostoslista",(shoplist.rect.left+13,shoplist.rect.top+13))
    shoppinglist = shoppingList.ShoppingList(xsGameFont,(shoplist.rect.left+13,shoplist.rect.top+50))

    # Timer
    timer = const.floorTime
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # Texts
    timerText = text.Text(mGameFont,time.strftime('%M:%S', time.gmtime(timer)),(screenSize[0]/2-45,screenSize[1]/2-341))
    checkpointText = text.Text(lGameFont,f'You have completed floor {floorNumber}', (screenSize[0]/2-370,screenSize[1]/6))
    debugText = text.Text(sGameFont,f'Detected fingers: {fingerPositions}',(20,20))

    def updateAllPositions(newScreenSize):
        #if gameStatus == "level":
        screenMove = (newScreenSize[0]-screenSize[0], newScreenSize[1]-screenSize[1])
        lobby.updatePos((newScreenSize[0]/2,newScreenSize[1]/2))
        room1.updatePos((newScreenSize[0]/2,newScreenSize[1]/2))
        player.updatePos(screenMove)
        downButton.updatePos((newScreenSize[0]-115*const.scale,newScreenSize[1]-69*const.scale))
        rightButton.updatePos((newScreenSize[0]-69*const.scale,newScreenSize[1]-115*const.scale))
        upButton.updatePos((newScreenSize[0]-115*const.scale,newScreenSize[1]-161*const.scale))
        leftButton.updatePos((newScreenSize[0]-161*const.scale,newScreenSize[1]-115*const.scale))
        exitButton.updatePos((newScreenSize[0]-231*const.scale,newScreenSize[1]-115*const.scale))
        frame.updatePos((newScreenSize[0]/2,newScreenSize[1]/2))
        timerText.updatePos((newScreenSize[0]/2-45,newScreenSize[1]/2-341))
        shoplist.updatePos((newScreenSize[0] - room1.rect.left/2, newScreenSize[1]/4))
        shoplistTitle.updatePos((shoplist.rect.left+13,shoplist.rect.top+13))
        shoppinglist.updatePos((shoplist.rect.left+13,shoplist.rect.top+50))
        #elif gameStatus == "checkpoint":
        checkpointText.updatePos((newScreenSize[0]/2-370,newScreenSize[1]/6))
        nextFloorButton.updatePos((newScreenSize[0]/2,newScreenSize[1]*3/4))
    
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
            # Advance timer
            elif event.type == pygame.USEREVENT and gameStatus == "level": 
                timer -= 1


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
        elif gameStatus == "level":

            # Check if any buttons are pressed
            for b in moveButtons:
                b.unpress()
                for pos in fingerPositions.values():
                    if b.rect.collidepoint(pos):
                        b.press()

            # Draw images to screen
            screen.fill(backg)                                          # BG
            room1.draw(screen)                                          # Room/tiles
            player.draw(screen)                                         # player
            player.update(room1)                                        # player actions
            for b in moveButtons:                                       # buttons
                b.draw(screen)               
            frame.draw(screen)                                          # room frame
            shoplist.draw(screen)                                       # shopping list
            shoplistTitle.draw(screen)
            shoppinglist.draw(screen)
            timerText.draw(screen,time.strftime('%M:%S', time.gmtime(timer)))                           # timer
            if room1.exit != None and room1.exit.rect.colliderect(player.rect):
                exitButton.draw(screen)                                 # exit button, if player is at the lift
                exitButton.unpress()
                for pos in fingerPositions.values():
                    if exitButton.rect.collidepoint(pos): # Go to the checkpoint lift
                        # exitButton.press()
                        gameStatus = "checkpoint" # Change the game status


        #########################################################
        # CHECKPOINT IN BETWEEN LEVELS
        #########################################################
        elif gameStatus == "checkpoint":
            screen.fill(backg)

            lobby.draw(screen)
            player.draw(screen)
            player.update(lobby)

            checkpointText.draw(screen,f'You have completed floor {floorNumber}')
            nextFloorButton.draw(screen)

            # Check if nextFloorButton is pressed
            for pos in fingerPositions.values():
                if nextFloorButton.rect.collidepoint(pos): # Go to next floor / start a new level
                    # nextFloorButton.press()
                    floorNumber += 1 # Advance floor number
                    gameStatus = "level" # Change game status
                    room1 = room.Room(const.roomLayouts[floorNumber % 3],(screenSize[0]/2,screenSize[1]/2)) # Create a new room
                    player.resetPos(screenSize) # Move player to the middle
                    timer = const.floorTime # Reset timer

        # Update all positions if the screen size is changed
        newScreenSize = pygame.display.get_window_size()
        if newScreenSize != screenSize:
            updateAllPositions(newScreenSize)
            screenSize = newScreenSize

        # Debug screen info
        if debugMode:
            debugText.draw(screen,f"Detected fingers: {fingerPositions} – FPS: {round(clock.get_fps())}")

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
        

asyncio.run(main())