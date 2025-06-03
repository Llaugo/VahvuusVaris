from sys import exit
import pygame
import constants
import playerClass
import random
import math




pygame.init()
clock = pygame.time.Clock()

player = pygame.sprite.GroupSingle() # Create the player sprite and attach a new player to it
player.add(playerClass.Player())

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    player.draw(constants.screen)
    player.update()

    pygame.display.update()
    clock.tick(60)
    