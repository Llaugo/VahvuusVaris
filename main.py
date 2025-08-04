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
import strengthMenu
import cart
import npc
import tradeMenu
import random
import math
import time



pygame.init()
clock = pygame.time.Clock() # Init clock
seed = random.random() # Set the seed
random.seed(seed)
print(seed)

screen = pygame.display.set_mode((const.worldWidth,const.worldHeight), pygame.RESIZABLE) # Set up screen

# Initialize buttons
downButton = button.Button(0,0,(0,0),const.scale)
rightButton = button.Button(2,0,(0,0),const.scale)
upButton = button.Button(4,0,(0,0),const.scale)
leftButton = button.Button(6,0,(0,0),const.scale)
moveButtons = [downButton, rightButton, upButton, leftButton]
liftButton = button.Button(10,1,(0,0),const.scale, const.gameFont(19), "HISSIIN", (8,63,6)) # Button to exit a level
# Checkpoint buttons
nextFloorButton = button.Button(0,4,(0,0),const.scale, const.gameFont(40), "Seuraava kerros", (8,63,6)) # Button to start a new level
# Menu buttons
startButton = button.Button(16,1,(0,0),const.scale)
continueButton = button.Button(16,1,(0,0),const.scale)
settingsButton = button.Button(16,1,(0,0),const.scale)
infoButton = button.Button(16,1,(0,0),const.scale)


# All buttons are handled from this array
buttons = [downButton,rightButton,upButton,leftButton,liftButton,nextFloorButton,startButton,continueButton,settingsButton,infoButton]

# Background color
backg = (160,209,255)
menuback = (180,200,215)
# Menu elements
menuBackground = picture.Picture("images/menu_screen.png", (4000,2000), (0,0), 0.45)
strengthPicker = strengthMenu.StrengthMenu()

shoppinglist = shoppingList.ShoppingList((0,0))

async def main():

    # If active, shows useful information about the game. (For debug purposes)
    debugMode = False
    screenSize = pygame.display.get_window_size() # Used to check changes in screen size

    # gameStatus: Shows the state of the game
    #   "level": Game is running a level
    #   "menu": Game is at the starting menu
    #   "strengths": Game is at the strength picking menu
    #   "checkpoint": Game is at a state in between levels
    gameStatus = "strengths"

    # Tracks the floor/level the player is at
    floorNumber = 1
    # The main floor object
    floor = floorClass.Floor(const.floorSize, floorNumber, moveButtons, shoppinglist)
    lobby = room.Room(const.lobbyLayout[0])
    deck = strengthDeck.StrengthDeck(strengthPicker.getDeck())


    # Texts
    checkpointText = text.Text(const.gameFont(50), f'Kerros {floorNumber} suoritettu.', (0,0))   # Checkpoint text
    debugText = text.Text(const.gameFont(20), f'FPS: {round(clock.get_fps())}',(20,20))          # Debug text

    # Updates all positions of all elements on the screen, when the screen size is changed
    def updateAllPositions(newScreenSize):
        screenMove = (newScreenSize[0]-screenSize[0], newScreenSize[1]-screenSize[1])
        newCenter = (newScreenSize[0]/2,newScreenSize[1]/2)
        lobby.updatePos(newCenter, (0,0))
        floor.updatePos(newScreenSize, newCenter, screenMove)
        downButton.updatePos((newScreenSize[0]-138,newScreenSize[1]-50))
        rightButton.updatePos((newScreenSize[0]-50,newScreenSize[1]-138))
        upButton.updatePos((newScreenSize[0]-138,newScreenSize[1]-225))
        leftButton.updatePos((newScreenSize[0]-225,newScreenSize[1]-138))
        liftButton.updatePos((floor.currentRoom.rect.right+80,newScreenSize[1]/2))
        if deck:
            deck.updatePos((floor.currentRoom.rect.left, newScreenSize[1]/2))
        checkpointText.updatePos((newScreenSize[0]/2,newScreenSize[1]/6),True)
        nextFloorButton.updatePos((newScreenSize[0]/2,newScreenSize[1]*4/5))
        startButton.updatePos((newScreenSize[0]/2-330, newScreenSize[1]/2-107))
        continueButton.updatePos((newScreenSize[0]/2-330, newScreenSize[1]/2+14))
        settingsButton.updatePos((newScreenSize[0]/2-330, newScreenSize[1]/2+135))
        infoButton.updatePos((newScreenSize[0]/2-330, newScreenSize[1]/2+256))
        menuBackground.updatePos(newCenter)
        strengthPicker.updatePos(newCenter)
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
                if deck:
                    deck.handleCards(event, screenSize)
                strengthPicker.handleEvent(event, screenSize)
                floor.handleButtons(event, screenSize)

        #########################################################
        # THE MAIN MENU
        #########################################################a
        if gameStatus == "menu":
            screen.fill(menuback)
            menuBackground.draw(screen)
            startButton.draw(screen)
            continueButton.draw(screen)
            settingsButton.draw(screen)
            infoButton.draw(screen)
            if startButton.pressComplete:
                startButton.unpress()
                gameStatus = "strengths"

        # THE STRENGTH MENU
        if gameStatus == "strengths":
            screen.fill(menuback)
            menuBackground.draw(screen)
            strengthPicker.draw(screen)
            if strengthPicker.backButton.pressComplete:
                strengthPicker.backButton.unpress()
                gameStatus = "menu"
            if strengthPicker.randomizeButton.pressComplete:
                strengthPicker.randomizeButton.unpress()
                strengthPicker.randomizeFavo()
            if strengthPicker.readyButton.pressComplete:
                strengthPicker.readyButton.unpress()
                gameStatus = "level"
                deck = strengthDeck.StrengthDeck(strengthPicker.getDeck())
                deck.updatePos((floor.currentRoom.rect.left, newScreenSize[1]/2))



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
            deck.update(floor)
            deck.draw(screen)                                                   # Strength deck

            # Draw the exit button, if player is at the exit
            if floor.currentRoom.exit != None and floor.currentRoom.exit.rect.colliderect(floor.player.rect):
                liftButton.draw(screen)
                if liftButton.pressComplete:
                    liftButton.unpress()
                    # EXIT THE LEVEL
                    gameStatus = "checkpoint" # Change the game status
                    deck.reset(floor) # Finish all active strengths
        

        #########################################################
        # CHECKPOINT IN BETWEEN LEVELS
        #########################################################
        elif gameStatus == "checkpoint":
            # Draw checkpoint elements
            screen.fill(backg)                                              # Background
            lobby.draw(screen, floor.player)                                              # Room
            floor.player.draw(screen)                                       # Player
            floor.player.update(lobby)
            checkpointText.draw(screen,f'Kerros {floorNumber} suoritettu.') # Text
            nextFloorButton.draw(screen)                                    # Next floor button

            # Check if nextFloorButton is pressed
            if nextFloorButton.pressComplete:
                nextFloorButton.unpress()
                # START NEW LEVEL
                gameStatus = "level"                        # Change game status
                floorNumber += 1                            # Advance floor number
                floor = floorClass.Floor(const.floorSize, floorNumber, moveButtons, shoppinglist)   # Create a new room
                floor.updatePos(screenSize,(screenSize[0]/2,screenSize[1]/2))
                floor.player.resetPos(screenSize)                 # Move player to the middle
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
        if debugMode and deck: # Show debug text info
            debugText.draw(screen, f"\nFPS: {round(clock.get_fps())} Seed: {seed}\nRoom loc: {floor.currentLocation} Player pos: {floor.player.pos}\nActive cards: {[c.timer for c in deck.cards]}\nCard cooldowns: {[c.cooldown for c in deck.cards]}\nN:{len(floor.currentRoom.items)} Items: {[floor.currentRoom.items[i].name + str(floor.currentRoom.items[i].rect.center) for i in range(len(floor.currentRoom.items))]}")

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
       

asyncio.run(main())