import pygame
import const
import text
import picture
import spriteSheet
from random import randint

# Class for the listing the wanted items. Has also the accompanied images and texts.
class ShoppingList():
    # titleFont: font for the title text
    # textFont: font for the (smaller) text used for the item list
    # pos: position of the list on the screen
    # lang: language of the game
    def __init__(self, pos, lang):
        # self.contents has 5 lists of type [item name, items posessed, items needed] for each item rarity level
        self.pos = pos
        self.lang = lang
        self.contents = []
        self.contents.append([const.shop(self.lang)[4][randint(0,4)],0,1]) # Item from each rarity level is picked at random
        self.contents.append([const.shop(self.lang)[3][randint(0,4)],0,2])
        self.contents.append([const.shop(self.lang)[2][randint(0,4)],0,4])
        self.contents.append([const.shop(self.lang)[1][randint(0,4)],0,6])
        self.contents.append([const.shop(self.lang)[0][randint(0,4)],0,10])
        self.back = picture.Picture("images/shoplist.png", (260,230), pos) # Background image
        self.title = text.Text(const.gameFont(), const.phrase[self.lang][7],(0,0)) # Title text
        self.text1 = text.Text(const.gameFont(14), [self.contents[i][0] for i in range(len(self.contents))], (0,0), (0,0,0), 10) # Item names
        self.text2 = text.Text(const.gameFont(14), [f'{self.contents[i][1]}/{self.contents[i][2]}' for i in range(len(self.contents))], (0,0),(0,0,0), 10, True) # item quantities / needs
        # Rest are for showing item icon upon receiving item
        self.itemSprite = spriteSheet.SpriteSheet('images/items.png')
        self.itemImage = self.itemSprite.getImage(0,46,46,const.scale)
        self.itemText = text.Text(const.gameFont(14), "404", (0,0), center=True)
        self.showImgTimer = 0
        self.filled = False

    def checkFillStatus(self):
        for con in self.contents:
            if con[1] != con[2]:
                return False
        self.filled = True
        return True

    # Add an item to collection if it is in the list
    # Returns True if item is needed and False if not
    # itemName: name of the received item
    def receiveItem(self, itemName):
        received = False
        for i in range(len(self.contents)):
            if self.contents[i][0] == itemName: # Check if item is in the list
                self.contents[i][1] = min(self.contents[i][1] + 1, self.contents[i][2]) # Increase item count
                self.text2.setText(f'{self.contents[i][1]}/{self.contents[i][2]}' for i in range(len(self.contents))) # Change display text
                imgNum = 0
                for i,name in enumerate([x for xs in const.shop(self.lang) for x in xs]): # Find item name in flattened list of all items
                    if name == itemName:
                        imgNum = i
                self.itemImage = self.itemSprite.getImage(imgNum,46,46,const.scale) # show item image
                self.showImgTimer = 100
                self.checkFillStatus()
                received = True
                break
        if received:
            self.itemText = text.Text(const.gameFont(16), str(itemName), (0,0), (0,194,0), center=True)
        else:
            self.itemText = text.Text(const.gameFont(16), str(itemName), (0,0), center=True)
            self.showImgTimer = -100
        self.updatePos(self.pos)
        return received
    
    def loseItem(self, itemI):
        self.contents[itemI] = [self.contents[itemI][0], self.contents[itemI][1]-1, self.contents[itemI][2]]
        self.text2.setText(f'{self.contents[i][1]}/{self.contents[i][2]}' for i in range(len(self.contents))) # Change display text
        self.updatePos(self.pos)

    # Update the pos of the list on the screen
    def updatePos(self, pos):
        self.pos = pos
        self.back.updatePos((pos[0] + self.back.rect.width/2 + 50, pos[1])) # update background
        self.title.updatePos((self.back.rect.left+10,self.back.rect.top+10)) # Update texts
        self.text1.updatePos((self.back.rect.left+13,self.back.rect.top+50))
        self.text2.updatePos((self.back.rect.right-34,self.back.rect.top+86))
        self.itemText.updatePos((self.back.rect.center[0], self.back.rect.bottom - 58))

    # Draw the list and the texts on the screen
    def draw(self, screen):
        self.back.draw(screen)  # Background
        self.title.draw(screen) # title
        self.text1.draw(screen) # names
        self.text2.draw(screen) # quantities
        if self.showImgTimer: # show item image if image timer is on
            self.itemText.draw(screen)
            if self.showImgTimer > 0:
                screen.blit(self.itemImage, (self.back.rect.center[0]-23, self.back.rect.bottom - 58))
                self.showImgTimer -= 1
            else:
                self.showImgTimer += 1

    def saveList(self):
        return self.contents

# listArr: [5x names, 5x quantities]
def listLoader(listArr, lang):
    list = ShoppingList((0,0), lang)
    list.contents = listArr
    return list
