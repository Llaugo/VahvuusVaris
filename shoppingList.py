import pygame
import const
import text
import picture
import spriteSheet
from random import randint


class ShoppingList():
    def __init__(self, titleFont, textFont, pos):
        # self.contents has 5 lists of type [item name, items posessed, items needed] for each item rarity level
        self.pos = pos
        self.contents = []
        self.contents.append([const.shop[4][randint(0,4)],0,1])
        self.contents.append([const.shop[3][randint(0,4)],0,2])
        self.contents.append([const.shop[2][randint(0,4)],0,4])
        self.contents.append([const.shop[1][randint(0,4)],0,6])
        self.contents.append([const.shop[0][randint(0,4)],0,10])
        self.back = picture.Picture("images/shoplist.png", (230,230), pos)
        self.title = text.Text(titleFont, "Ostoslista",(self.back.rect.left+13,self.back.rect.top+13))
        self.text1 = text.Text(textFont, [self.contents[i][0] for i in range(len(self.contents))], (self.back.rect.left+13,self.back.rect.top+50), (0,0,0), 10)
        self.text2 = text.Text(textFont, [f'{self.contents[i][1]} / {self.contents[i][2]}' for i in range(len(self.contents))], (self.back.rect.right-55,self.back.rect.top+50),(0,0,0), 10)
        
        itemSpriteSheet = pygame.image.load('images/items.png').convert() # Load items' spritesheet
        self.itemSprite = spriteSheet.SpriteSheet(itemSpriteSheet)
        self.itemImage = self.itemSprite.getImage(0,46,46,const.scale)
        self.showImgTimer = 0

    # Add a item to collection if it is in the list
    # Returns True if item is needed and False if not
    def receiveItem(self, itemName):
        for i in range(len(self.contents)):
            if self.contents[i][0] == itemName:
                self.contents[i][1] = min(self.contents[i][1] + 1, self.contents[i][2])
                self.text2.setText(f'{self.contents[i][1]} / {self.contents[i][2]}' for i in range(len(self.contents)))
                imgNum = 0
                for i,name in enumerate([x for xs in const.shop for x in xs]):
                    if name == itemName:
                        imgNum = i
                self.itemImage = self.itemSprite.getImage(imgNum,46,46,const.scale)
                self.showImgTimer = 100
                return True
        return False

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
        if self.showImgTimer > 0:
            screen.blit(self.itemImage, (self.back.rect.center[0]-23, self.back.rect.bottom - 60))
            self.showImgTimer -= 1
