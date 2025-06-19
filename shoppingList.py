import pygame
import const
import text
from random import randint


class ShoppingList():
    def __init__(self, font, pos):
        # self.contents has 5 tuplets of type (item name, items posessed, items needed) for each item rarity level
        self.font = font
        self.pos = pos
        self.contents = []
        self.contents.append((const.shop[0][randint(0,4)],0,1))
        self.contents.append((const.shop[1][randint(0,4)],0,1))
        self.contents.append((const.shop[2][randint(0,4)],0,2))
        self.contents.append((const.shop[3][randint(0,4)],0,5))
        self.contents.append((const.shop[4][randint(0,4)],0,10))
        self.listItem1 = text.Text(self.font,f"{self.contents[0][0]}",self.pos)
        self.listItem2 = text.Text(self.font,f"{self.contents[1][0]}",(self.pos[0],self.pos[1]+25))
        self.listItem3 = text.Text(self.font,f"{self.contents[2][0]}",(self.pos[0],self.pos[1]+50))
        self.listItem4 = text.Text(self.font,f"{self.contents[3][0]}",(self.pos[0],self.pos[1]+75))
        self.listItem5 = text.Text(self.font,f"{self.contents[4][0]}",(self.pos[0],self.pos[1]+100))

    def updatePos(self, pos):
        self.pos = pos
        self.listItem1.updatePos(self.pos)
        self.listItem2.updatePos((self.pos[0],self.pos[1]+25))
        self.listItem3.updatePos((self.pos[0],self.pos[1]+50))
        self.listItem4.updatePos((self.pos[0],self.pos[1]+75))
        self.listItem5.updatePos((self.pos[0],self.pos[1]+100))

    def draw(self, screen):
        self.listItem1.draw(screen)
        self.listItem2.draw(screen)
        self.listItem3.draw(screen)
        self.listItem4.draw(screen)
        self.listItem5.draw(screen)
