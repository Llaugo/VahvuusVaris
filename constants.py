import pygame


worldHeight = 1000
worldWidth = 1000
scale = 1.5


playerSpeed = 3
playerImg = [[pygame.transform.rotozoom(pygame.image.load('images/pl_ph_ala1.png').convert(),0,scale),
             pygame.transform.rotozoom(pygame.image.load('images/pl_ph_ala2.png').convert(),0,scale),
             pygame.transform.rotozoom(pygame.image.load('images/pl_ph_ala3.png').convert(),0,scale),
             pygame.transform.rotozoom(pygame.image.load('images/pl_ph_ala4.png').convert(),0,scale)],
             [pygame.transform.rotozoom(pygame.image.load('images/pl_ph_oik1.png').convert(),0,scale),
             pygame.transform.rotozoom(pygame.image.load('images/pl_ph_oik2.png').convert(),0,scale),
             pygame.transform.rotozoom(pygame.image.load('images/pl_ph_oik3.png').convert(),0,scale),
             pygame.transform.rotozoom(pygame.image.load('images/pl_ph_oik4.png').convert(),0,scale)],
             [pygame.transform.rotozoom(pygame.image.load('images/pl_ph_ylä1.png').convert(),0,scale),
             pygame.transform.rotozoom(pygame.image.load('images/pl_ph_ylä2.png').convert(),0,scale),
             pygame.transform.rotozoom(pygame.image.load('images/pl_ph_ylä3.png').convert(),0,scale),
             pygame.transform.rotozoom(pygame.image.load('images/pl_ph_ylä4.png').convert(),0,scale)],
             [pygame.transform.rotozoom(pygame.image.load('images/pl_ph_vas1.png').convert(),0,scale),
             pygame.transform.rotozoom(pygame.image.load('images/pl_ph_vas2.png').convert(),0,scale),
             pygame.transform.rotozoom(pygame.image.load('images/pl_ph_vas3.png').convert(),0,scale),
             pygame.transform.rotozoom(pygame.image.load('images/pl_ph_vas4.png').convert(),0,scale)]]