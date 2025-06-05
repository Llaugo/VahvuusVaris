from sys import exit
import asyncio # For creating a browser view
import pygame
import constants
import spriteSheet
import playerClass
import button
import random
import math




pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((constants.worldWidth,constants.worldHeight)) # Set screen size

# Buttons for moving
downButton = button.Button(0,(constants.worldWidth-115*constants.scale,constants.worldHeight-69*constants.scale),constants.scale,screen)
rightButton = button.Button(2,(constants.worldWidth-69*constants.scale,constants.worldHeight-115*constants.scale),constants.scale,screen)
upButton = button.Button(4,(constants.worldWidth-115*constants.scale,constants.worldHeight-161*constants.scale),constants.scale,screen)
leftButton = button.Button(6,(constants.worldWidth-161*constants.scale,constants.worldHeight-115*constants.scale),constants.scale,screen)
buttons = [downButton, rightButton, upButton, leftButton]
buttonsPressed = {} 

# Player
player = pygame.sprite.GroupSingle() # Create the player sprite and attach a new player to it
player.add(playerClass.Player(screen,buttons))



backg = (100,100,100)

async def main():

    # If active, shows useful information about the game. (For debug purposes)
    debugMode = True
    
    # Main game loop
    while True:
        # Event handler
        for event in pygame.event.get():
            # Quitting the game and closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Observe finger touches on the movement buttons
            if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERMOTION:
                x = event.x * constants.worldWidth
                y = event.y * constants.worldHeight
                buttonsPressed[event.finger_id] = (x,y)
            elif event.type == pygame.FINGERUP:
                buttonsPressed.pop(event.finger_id)
            # Observe mouse presses on the movement buttons
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                buttonsPressed["mousePress"] = pos
            elif event.type == pygame.MOUSEBUTTONUP:
                buttonsPressed.pop("mousePress")
        # Activate debug mode
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            debugMode = not debugMode 

        for b in buttons:
            b.unpress()
            for pos in buttonsPressed.values():
                if b.rect.collidepoint(pos):
                    b.press()

        # Draw images to screen
        screen.fill(backg)
        player.draw(screen)
        player.update()
        for b in buttons: b.draw(screen)


        if debugMode:
            debugfont = pygame.font.SysFont("fontname", 30)
            debug_surf = debugfont.render(f'Detected fingers: {buttonsPressed}',False,(50,50,50))
            debug_rect = debug_surf.get_rect(topleft = (10,10))
            screen.blit(debug_surf,debug_rect)

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
        

asyncio.run(main())