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

# Player initialization
player = playerClass.Player(moveButtons, (const.worldWidth/2,const.worldHeight/2))
# Strength deck initialization
deck = strengthDeck.StrengthDeck((2,3,18,21,22,25),const.xxsGameFont)

# Background color
backg = (160,209,255)

async def main():

    # If active, shows useful information about the game. (For debug purposes)
    debugMode = False
    screenSize = pygame.display.get_window_size() # Used to check changes in screen size

    # gameStatus: Shows the state of the game
    #   "level": Game is running a level
    #   "menu": Game is at the starting menu
    #   "checkpoint": Game is at a state in between levels
    gameStatus = "level"

    # Tracks the floor/level the player is at
    floorNumber = 1
    # Test rooms
    room1 = room.Room(const.roomLayouts[0],(0,0))
    lobby = room.Room(const.lobbyLayout, (0,0))
    # Frame image for game area
    frame = picture.Picture("images/frame.png", (710,710), (0,0))

    # Shopping list
    shoppinglist = shoppingList.ShoppingList(const.sGameFont, const.xsGameFont,(0,0))

    # Timer
    timer = const.floorTime
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # Texts
    floorText = text.Text(const.mGameFont, f'Kerros {floorNumber}', (0,0))                    # Floor number
    timerText = text.Text(const.mGameFont, time.strftime('%M:%S',time.gmtime(timer)),(0,0))   # Timer
    checkpointText = text.Text(const.lGameFont, f'Kerros {floorNumber} suoritettu.', (0,0))   # Checkpoint text
    debugText = text.Text(const.sGameFont, f'FPS: {round(clock.get_fps())}',(20,20))          # Debug text

    # Updates all positions of all elements on the screen, when the screen size is changed
    def updateAllPositions(newScreenSize):
        screenMove = (newScreenSize[0]-screenSize[0], newScreenSize[1]-screenSize[1])
        lobby.updatePos((newScreenSize[0]/2,newScreenSize[1]/2), (0,0))
        room1.updatePos((newScreenSize[0]/2,newScreenSize[1]/2), screenMove)
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
        deck.updatePos((room1.rect.left, newScreenSize[1]/2))
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
            # Advance timer
            elif event.type == pygame.USEREVENT and gameStatus == "level": 
                timer -= 1
            # Handle button presses
            else:
                for btn in buttons:
                    btn.handleEvent(event, screenSize)
                deck.handleButtons(event, screenSize)


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
            screen.fill(backg)                                                  # BG
            room1.draw(screen, player)                                                  # Room/tiles
            player.update(room1)                                                # player actions
            player.draw(screen)                                                 # player
            for b in moveButtons:                                               # buttons
                b.draw(screen)               
            frame.draw(screen)                                                  # room frame
            shoppinglist.draw(screen)                                           # shopping list
            floorText.draw(screen)                                              # Floor number
            timerText.draw(screen,time.strftime('%M:%S', time.gmtime(timer)))   # timer
            deck.update(player, room1)
            deck.draw(screen)                                                   # Strength deck

            
            # Picking up items from the room
            for item in room1.items:
                if item.rect.colliderect(player.rect):  # Show the button if player is on top of the item
                    itemButton.draw(screen)
                    if itemButton.activeFinger:         # Take item if button is active
                        shoppinglist.receiveItem(item.name)
                        room1.removeItem(item)
            
            # Draw the exit button, if player is at the exit
            if room1.exit != None and room1.exit.rect.colliderect(player.rect):
                exitButton.draw(screen)
                if exitButton.activeFinger:
                    # EXIT THE LEVEL
                    gameStatus = "checkpoint" # Change the game status
                    deck.reset(player, room1) # Finish all active strengths
        

        #########################################################
        # CHECKPOINT IN BETWEEN LEVELS
        #########################################################
        elif gameStatus == "checkpoint":
            # Draw checkpoint elements
            screen.fill(backg)                                              # Background
            lobby.draw(screen, player)                                              # Room
            player.draw(screen)                                             # Player
            player.update(lobby)
            checkpointText.draw(screen,f'Kerros {floorNumber} suoritettu.') # Text
            nextFloorButton.draw(screen)                                    # Next floor button

            # Check if nextFloorButton is pressed
            if nextFloorButton.activeFinger:
                # START NEW LEVEL
                floorNumber += 1                            # Advance floor number
                floorText.setText(f'Kerros {floorNumber}')
                gameStatus = "level"                        # Change game status
                room1 = room.Room(const.roomLayouts[floorNumber % 4],(screenSize[0]/2,screenSize[1]/2)) # Create a new room
                player.resetPos(screenSize)                 # Move player to the middle
                timer = const.floorTime                     # Reset timer
                #deck.reset(player, room1)                   # Reset the card deck

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
            debugText.draw(screen, f"FPS: {round(clock.get_fps())} Seed: {seed}\nActive cards: {[c.timer for c in deck.cards]}\nCard cooldowns: {[c.cooldown for c in deck.cards]}\nN:{len(room1.items)} Items: {[room1.items[i].name + str(room1.items[i].rect.center) for i in range(len(room1.items))]}")

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
        

asyncio.run(main())