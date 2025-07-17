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
import floorClass
import random
import math
import time



pygame.init()
clock = pygame.time.Clock() # Init clock
seed = random.random() # Set the seed
random.seed(seed)
print(seed)

screen = pygame.display.set_mode((const.worldWidth,const.worldHeight), pygame.RESIZABLE) # Set up screen

# Initialize buttons for moving
downButton = button.Button(0,(0,0),const.scale)
rightButton = button.Button(2,(0,0),const.scale)
upButton = button.Button(4,(0,0),const.scale)
leftButton = button.Button(6,(0,0),const.scale)
moveButtons = [downButton, rightButton, upButton, leftButton]
exitButton = button.Button(10,(0,0),const.scale, const.sGameFont, "HISSIIN", (8,63,6)) # Button to exit a level
nextFloorButton = button.Button(10,(0,0),const.scale, const.xsGameFont, "SEURAAVA\n  KERROS", (8,63,6)) # Button to start a new level
itemButton = button.Button(14,(0,0),const.scale, const.sGameFont, " OTA\nESINE", (130,63,0)) # Button to pick up items
# All buttons are handled from this array
buttons = [downButton,rightButton,upButton,leftButton,exitButton,nextFloorButton,itemButton]

# Strength deck initialization
deck = strengthDeck.StrengthDeck((4,8,18,19,24,25),const.xxsGameFont)

# Background color
backg = (160,209,255)

async def main():

    # If active, shows useful information about the game. (For debug purposes)
    debugMode = True
    screenSize = pygame.display.get_window_size() # Used to check changes in screen size

    # gameStatus: Shows the state of the game
    #   "level": Game is running a level
    #   "menu": Game is at the starting menu
    #   "checkpoint": Game is at a state in between levels
    gameStatus = "level"

    # Tracks the floor/level the player is at
    floorNumber = 1
    # The main floor object
    floor = floorClass.Floor(const.floorSize, floorNumber, moveButtons)
    lobby = room.Room(const.lobbyLayout)

    # Shopping list
    shoppinglist = shoppingList.ShoppingList(const.sGameFont, const.xsGameFont,(0,0))

    # Texts
    checkpointText = text.Text(const.lGameFont, f'Kerros {floorNumber} suoritettu.', (0,0))   # Checkpoint text
    debugText = text.Text(const.sGameFont, f'FPS: {round(clock.get_fps())}',(20,20))          # Debug text

    # Updates all positions of all elements on the screen, when the screen size is changed
    def updateAllPositions(newScreenSize):
        screenMove = (newScreenSize[0]-screenSize[0], newScreenSize[1]-screenSize[1])
        lobby.updatePos((newScreenSize[0]/2,newScreenSize[1]/2), (0,0))
        floor.updatePos((newScreenSize[0]/2,newScreenSize[1]/2), screenMove)
        downButton.updatePos((newScreenSize[0]-138,newScreenSize[1]-50))
        rightButton.updatePos((newScreenSize[0]-50,newScreenSize[1]-138))
        upButton.updatePos((newScreenSize[0]-138,newScreenSize[1]-225))
        leftButton.updatePos((newScreenSize[0]-225,newScreenSize[1]-138))
        exitButton.updatePos((newScreenSize[0]/2+460,newScreenSize[1]/2))
        shoppinglist.updatePos((newScreenSize[0] - floor.currentRoom.rect.left/2, newScreenSize[1]/4))
        itemButton.updatePos((newScreenSize[0]/2+580,newScreenSize[1]/2))
        deck.updatePos((floor.currentRoom.rect.left, newScreenSize[1]/2))
        checkpointText.updatePos((newScreenSize[0]/2,newScreenSize[1]/6),True)
        nextFloorButton.updatePos((newScreenSize[0]/2,newScreenSize[1]*4/5))
    # Called once at the start to get everything in place
    updateAllPositions(screenSize)

    # Main game loop
    while True:
        # Event handler
        for event in pygame.event.get():
            # Quitting the game and closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Handle button presses
            else:
                for btn in buttons:
                    btn.handleEvent(event, screenSize)
                deck.handleButtons(event, screenSize)


        #########################################################
        # THE MAIN MENU
        #########################################################a
        if gameStatus == "menu":
            pass


        #########################################################
        # RUNNING A LEVEL
        #########################################################
        elif gameStatus == "level":

            # Draw images to screen
            screen.fill(backg)                                                  # BG
            floor.update()
            floor.draw(screen)                                   # current room
            for b in moveButtons:                                               # buttons
                b.draw(screen)               
            shoppinglist.draw(screen)                                           # shopping list
            deck.update(floor)
            deck.draw(screen)                                                   # Strength deck

            # Picking up items from the room
            for item in floor.currentRoom.items:
                if item.rect.colliderect(floor.player.rect):  # Show the button if player is on top of the item
                    itemButton.draw(screen)
                    if itemButton.activeFinger:         # Take item if button is active
                        shoppinglist.receiveItem(item.name)
                        floor.currentRoom.removeItem(item)

            # Draw the exit button, if player is at the exit
            if floor.currentRoom.exit != None and floor.currentRoom.exit.rect.colliderect(floor.player.rect):
                exitButton.draw(screen)
                if exitButton.activeFinger:
                    # EXIT THE LEVEL
                    gameStatus = "checkpoint" # Change the game status
                    deck.reset(floor) # Finish all active strengths
        

        #########################################################
        # CHECKPOINT IN BETWEEN LEVELS
        #########################################################
        elif gameStatus == "checkpoint":
            # Draw checkpoint elements
            screen.fill(backg)                                              # Background
            lobby.draw(screen)                                              # Room
            floor.player.draw(screen)                                       # Player
            floor.player.update(lobby)
            checkpointText.draw(screen,f'Kerros {floorNumber} suoritettu.') # Text
            nextFloorButton.draw(screen)                                    # Next floor button

            # Check if nextFloorButton is pressed
            if nextFloorButton.activeFinger:
                # START NEW LEVEL
                gameStatus = "level"                        # Change game status
                floorNumber += 1                            # Advance floor number
                floor = floorClass.Floor(const.floorSize, floorNumber, moveButtons)   # Create a new room
                floor.updatePos((screenSize[0]/2,screenSize[1]/2))
                floor.player.resetPos(screenSize)                 # Move player to the middle
                timer = const.floorTime                     # Reset timer
                #deck.reset(player, floor)                   # Reset the card deck

        # Update all positions if the screen size is changed
        newScreenSize = pygame.display.get_window_size()
        if newScreenSize != screenSize:
            updateAllPositions(newScreenSize)
            screenSize = newScreenSize

        # Toggle debug mode
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]: # Show debug on pressing the R-key
            debugMode = not debugMode
        if debugMode: # Show debug text info
            debugText.draw(screen, f"FPS: {round(clock.get_fps())} Seed: {seed}\nRoom loc: {floor.currentLocation} Player pos: {floor.player.pos}\nActive cards: {[c.timer for c in deck.cards]}\nCard cooldowns: {[c.cooldown for c in deck.cards]}\nN:{len(floor.currentRoom.items)} Items: {[floor.currentRoom.items[i].name + str(floor.currentRoom.items[i].rect.center) for i in range(len(floor.currentRoom.items))]}")

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
       

asyncio.run(main())