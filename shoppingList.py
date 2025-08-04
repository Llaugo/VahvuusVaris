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
    def __init__(self, pos):
        # self.contents has 5 lists of type [item name, items posessed, items needed] for each item rarity level
        self.pos = pos
        self.contents = []
        self.contents.append([const.shop[4][randint(0,4)],0,1]) # Item from each rarity level is picked at random
        self.contents.append([const.shop[3][randint(0,4)],0,2])
        self.contents.append([const.shop[2][randint(0,4)],0,4])
        self.contents.append([const.shop[1][randint(0,4)],0,6])
        self.contents.append([const.shop[0][randint(0,4)],5,10])
        self.back = picture.Picture("images/shoplist.png", (260,230), pos) # Background image
        self.title = text.Text(const.gameFont(), "Ostoslista",(0,0)) # Title text
        self.text1 = text.Text(const.gameFont(14), [self.contents[i][0] for i in range(len(self.contents))], (0,0), (0,0,0), 10) # Item names
        self.text2 = text.Text(const.gameFont(14), [f'{self.contents[i][1]}/{self.contents[i][2]}' for i in range(len(self.contents))], (0,0),(0,0,0), 10) # item quantities / needs
        # Rest are for showing item icon upon receiving item
        itemSpriteSheet = pygame.image.load('images/items.png').convert() # Load items' spritesheet
        self.itemSprite = spriteSheet.SpriteSheet(itemSpriteSheet)
        self.itemImage = self.itemSprite.getImage(0,46,46,const.scale)
        self.showImgTimer = 0

    # Add an item to collection if it is in the list
    # Returns True if item is needed and False if not
    # itemName: name of the received item
    def receiveItem(self, itemName):
        for i in range(len(self.contents)):
            if self.contents[i][0] == itemName: # Check if item is in the list
                self.contents[i][1] = min(self.contents[i][1] + 1, self.contents[i][2]) # Increase item count
                self.text2.setText(f'{self.contents[i][1]}/{self.contents[i][2]}' for i in range(len(self.contents))) # Change display text
                imgNum = 0
                for i,name in enumerate([x for xs in const.shop for x in xs]): # Find item name in flattened list of all items
                    if name == itemName:
                        imgNum = i
                self.itemImage = self.itemSprite.getImage(imgNum,46,46,const.scale) # show item image
                self.showImgTimer = 100
                return True
        return False
    
    def loseItem(self, itemI):
        self.contents[itemI] = [self.contents[itemI][0], self.contents[itemI][1]-1, self.contents[itemI][2]]
        self.text2.setText(f'{self.contents[i][1]}/{self.contents[i][2]}' for i in range(len(self.contents))) # Change display text

    # Update the pos of the list on the screen
    def updatePos(self, pos):
        self.pos = pos
        self.back.updatePos(pos) # update background
        self.title.updatePos((self.back.rect.left+10,self.back.rect.top+10)) # Update texts
        self.text1.updatePos((self.back.rect.left+13,self.back.rect.top+50))
        self.text2.updatePos((self.back.rect.right-48,self.back.rect.top+50))

    # Draw the list and the texts on the screen
    def draw(self, screen):
        self.back.draw(screen)  # Background
        self.title.draw(screen) # title
        self.text1.draw(screen) # names
        self.text2.draw(screen) # quantities
        if self.showImgTimer > 0: # show item image if image timer is on
            screen.blit(self.itemImage, (self.back.rect.center[0]-23, self.back.rect.bottom - 60))
            self.showImgTimer -= 1
