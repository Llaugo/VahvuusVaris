import pygame
import const
import text
import picture
from random import randint


class ShoppingList():
    def __init__(self, titleFont, textFont, pos):
        # self.contents has 5 tuplets of type (item name, items posessed, items needed) for each item rarity level
        self.pos = pos
        self.contents = []
        self.contents.append((const.shop[4][randint(0,4)],0,1))
        self.contents.append((const.shop[3][randint(0,4)],0,2))
        self.contents.append((const.shop[2][randint(0,4)],0,4))
        self.contents.append((const.shop[1][randint(0,4)],0,6))
        self.contents.append((const.shop[0][randint(0,4)],0,10))
        self.back = picture.Picture("images/shoplist.png", (230,230), pos)
        self.title = text.Text(titleFont, "Ostoslista",(self.back.rect.left+13,self.back.rect.top+13))
        self.text1 = text.Text(textFont, [self.contents[i][0] for i in range(len(self.contents))], (self.back.rect.left+13,self.back.rect.top+50), (0,0,0), 10)
        self.text2 = text.Text(textFont, [f'{self.contents[i][1]} / {self.contents[i][2]}' for i in range(len(self.contents))], (self.back.rect.right-55,self.back.rect.top+50),(0,0,0), 10)

    def updatePos(self, pos):
        self.pos = pos
        self.back.updatePos(pos)
        self.title.updatePos((self.back.rect.left+13,self.back.rect.top+13))
        self.text1.updatePos((self.back.rect.left+13,self.back.rect.top+50))
        self.text2.updatePos((self.back.rect.right-55,self.back.rect.top+50))

    def draw(self, screen):
        self.back.draw(screen)
        self.title.draw(screen)
        self.text1.draw(screen)
        self.text2.draw(screen)
