#!/usr/bin/env pypy
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
import item
import strengthCard
import strengthDeck
import random
import math
import time



pygame.init()
clock = pygame.time.Clock()
seed = random.random()
random.seed(seed)
print(seed)

screen = pygame.display.set_mode((const.worldWidth,const.worldHeight), pygame.RESIZABLE) # Set screen size

# Different font sizes
xsGameFont = pygame.font.SysFont(None, 23)
sGameFont = pygame.font.SysFont(None, 30)
mGameFont = pygame.font.SysFont(None, 50)
lGameFont = pygame.font.SysFont(None, 80)

# Initialize buttons for moving
downButton = button.Button(0,(0,0),const.scale)
rightButton = button.Button(2,(0,0),const.scale)
upButton = button.Button(4,(0,0),const.scale)
leftButton = button.Button(6,(0,0),const.scale)
moveButtons = [downButton, rightButton, upButton, leftButton]
exitButton = button.Button(10,(0,0),const.scale, sGameFont, "HISSIIN", (8,63,6))
nextFloorButton = button.Button(10,(0,0),const.scale, xsGameFont, "SEURAAVA\n  KERROS", (8,63,6))
itemButton = button.Button(14,(0,0),const.scale, sGameFont, " OTA\nESINE", (130,63,0))
# All button are handled from this array
buttons = [downButton,rightButton,upButton,leftButton,exitButton,nextFloorButton,itemButton]

# Player initialization
player = playerClass.Player(moveButtons, (const.worldWidth/2,const.worldHeight/2))

deck = strengthDeck.StrengthDeck((0,1,2,3,4,5))

# Background color
backg = (160,209,255)


async def main():

    # If active, shows useful information about the game. (For debug purposes)
    debugMode = True
    screenSize = pygame.display.get_window_size()
    # gameStatus: Shows the state of the game
    #   "level": Game is running a level
    #   "menu": Game is at the starting menu
    #   "checkpoint": Game is at a state in between levels
    gameStatus = "level"
    # Tracks the floor/level the player is at
    floorNumber = 1

    room1 = room.Room(const.roomLayouts[0],(0,0))
    lobby = room.Room(const.lobbyLayout, (0,0))

    frame = picture.Picture("images/frame.png", (710,710), (0,0))

    # Shopping list
    shoppinglist = shoppingList.ShoppingList(sGameFont, xsGameFont,(0,0))

    # Timer
    timer = const.floorTime
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # Texts
    floorText = text.Text(mGameFont, f'Kerros {floorNumber}', (0,0))
    timerText = text.Text(mGameFont, time.strftime('%M:%S',time.gmtime(timer)),(0,0))
    checkpointText = text.Text(lGameFont, f'Kerros {floorNumber} suoritettu.', (0,0))
    debugText = text.Text(sGameFont, f'FPS: {round(clock.get_fps())}',(20,20))

    def updateAllPositions(newScreenSize):
        #if gameStatus == "level":
        screenMove = (newScreenSize[0]-screenSize[0], newScreenSize[1]-screenSize[1])
        lobby.updatePos((newScreenSize[0]/2,newScreenSize[1]/2))
        room1.updatePos((newScreenSize[0]/2,newScreenSize[1]/2))
        player.updatePos(screenMove)
        downButton.updatePos((newScreenSize[0]-138,newScreenSize[1]-50))
        rightButton.updatePos((newScreenSize[0]-50,newScreenSize[1]-138))
        upButton.updatePos((newScreenSize[0]-138,newScreenSize[1]-225))
        leftButton.updatePos((newScreenSize[0]-225,newScreenSize[1]-138))
        exitButton.updatePos((newScreenSize[0]/2+460,newScreenSize[1]/2))
        frame.updatePos((newScreenSize[0]/2,newScreenSize[1]/2))
        floorText.updatePos((newScreenSize[0]/2-340,newScreenSize[1]/2-341))
        timerText.updatePos((newScreenSize[0]/2-45,newScreenSize[1]/2-341))
        shoppinglist.updatePos((newScreenSize[0] - room1.rect.left/2, newScreenSize[1]/4))
        itemButton.updatePos((newScreenSize[0]/2+580,newScreenSize[1]/2))
        deck.updatePos((room1.rect.left, newScreenSize[1]))
        #elif gameStatus == "checkpoint":
        checkpointText.updatePos((newScreenSize[0]/2,newScreenSize[1]/6),True)
        nextFloorButton.updatePos((newScreenSize[0]/2,newScreenSize[1]*4/5))
    updateAllPositions(screenSize)

    # Main game loop
    while True:
        # Event handler
        for event in pygame.event.get():
            # Quitting the game and closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Advance timer
            elif event.type == pygame.USEREVENT and gameStatus == "level": 
                timer -= 1
            # Handle button presses
            else:
                for btn in buttons:
                    btn.handleEvent(event,screenSize)


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

            # Draw images to screen
            screen.fill(backg)                                          # BG
            room1.draw(screen)                                          # Room/tiles
            player.draw(screen)                                         # player
            player.update(room1)                                        # player actions
            for b in moveButtons:                                       # buttons
                b.draw(screen)               
            frame.draw(screen)                                          # room frame
            shoppinglist.draw(screen)                                   # shopping list
            floorText.draw(screen)
            timerText.draw(screen,time.strftime('%M:%S', time.gmtime(timer))) # timer
            deck.draw(screen)

            # Picking up items from the room
            for item in room1.items:
                if item.rect.colliderect(player.rect):
                    itemButton.draw(screen)
                    if itemButton.activeFinger:
                        shoppinglist.receiveItem(item.name)
                        room1.removeItem(item)
            
            # Draw the exit button, if player is at the exit
            if room1.exit != None and room1.exit.rect.colliderect(player.rect):
                exitButton.draw(screen)
                if exitButton.activeFinger:
                    gameStatus = "checkpoint" # Change the game status


        #########################################################
        # CHECKPOINT IN BETWEEN LEVELS
        #########################################################
        elif gameStatus == "checkpoint":
            screen.fill(backg)

            lobby.draw(screen)
            player.draw(screen)
            player.update(lobby)

            checkpointText.draw(screen,f'Kerros {floorNumber} suoritettu.')
            nextFloorButton.draw(screen)

            # Check if nextFloorButton is pressed
            if nextFloorButton.activeFinger:
                floorNumber += 1 # Advance floor number
                floorText.setText(f'Kerros {floorNumber}')
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
            debugText.draw(screen, f"FPS: {round(clock.get_fps())} Seed: {seed}\nN:{len(room1.items)} Items: {[room1.items[i].name + str(room1.items[i].rect.center) for i in range(len(room1.items))]}")

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
        

asyncio.run(main())