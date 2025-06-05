from sys import exit
import asyncio # For creating a browser view
import pygame
import constants
import spriteSheet
import playerClass
import random
import math




pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((constants.worldWidth,constants.worldHeight)) # Set screen size

player = pygame.sprite.GroupSingle() # Create the player sprite and attach a new player to it
player.add(playerClass.Player(screen))

async def main():

    
    
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        player.draw(screen)
        player.update()

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
        

asyncio.run(main())