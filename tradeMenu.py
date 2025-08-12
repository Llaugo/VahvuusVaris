import pygame
import picture
import text
import const
import button
import shoppingList


class TradeMenu():
    # lang: language of the game
    def __init__(self, list: shoppingList.ShoppingList, cart, pos, lang, doubleItem=False):
        self.pos = pos
        self.lang = lang
        self.list = list
        self.listItem = None
        self.itemI = 0
        for i in range(len(self.list.contents)):
            self.itemI = len(self.list.contents)-1-i
            content = self.list.contents[self.itemI]
            if content[1] > 0:
                self.listItem = content[0]
                break
        self.cart = cart
        self.doubleItem = doubleItem
        #self.pos = (0,0)
        self.background = picture.Picture("images/trade_view.png", (710,710), (0,0))
        self.infoText = text.Text(const.gameFont(46), const.phrase[self.lang][9],(0,0))
        self.oldItem = text.Text(const.gameFont(40), f"- {self.listItem}", (0,0), (255,0,0))
        self.newItem = text.Text(const.gameFont(40), f"+ {self.cart.item.name}", (0,0), (0,255,0))
        if doubleItem:
            self.newItem.setText(f"+ 2x {self.cart.item.name}")
        self.yesButton = button.Button(10,1,(0,0),const.scale, const.gameFont(23), const.phrase[self.lang][10])
        self.noButton = button.Button(12,1,(0,0),const.scale, const.gameFont(23), const.phrase[self.lang][11])
        self.changeButton = button.Button(14,1,(0,0),const.scale*0.6, const.gameFont(12), const.phrase[self.lang][5])
        self.doBlits(pos)
        
    def doBlits(self, pos):
        self.background = picture.Picture("images/trade_view.png", (710,710), (0,0))
        self.background.blitOnto(self.infoText.surfaces[0], (-self.infoText.surfaces[0].get_width()/2,-220), True)
        self.background.blitOnto(self.oldItem.surfaces[0], (-self.oldItem.surfaces[0].get_width()/2,-100), True)
        self.background.blitOnto(self.newItem.surfaces[0], (-self.newItem.surfaces[0].get_width()/2,-50), True)
        self.updatePos(pos)

    def confirmTrade(self):
        oldItem = self.cart.switchItem(self.listItem)
        self.list.receiveItem(oldItem.name)
        if self.doubleItem:
            self.list.receiveItem(oldItem.name)
        self.list.loseItem(self.itemI)

    def changeItem(self):
        for _ in range(len(self.list.contents)+1):
            self.itemI = (self.itemI-1) % len(self.list.contents)
            content = self.list.contents[self.itemI]
            if content[1] > 0:
                self.listItem = content[0]
                break
        self.oldItem = text.Text(const.gameFont(40), f"- {self.listItem}", (0,0), (255,0,0))
        self.doBlits(self.pos)

    def handleButtons(self, event, screenSize):
        self.yesButton.handleEvent(event, screenSize)
        self.noButton.handleEvent(event, screenSize)
        self.changeButton.handleEvent(event, screenSize)
        if self.changeButton.pressComplete:
            self.changeButton.unpress()
            self.changeItem()

    def updatePos(self, screenCenter):
        self.pos = screenCenter
        self.background.updatePos(screenCenter)
        self.yesButton.updatePos((screenCenter[0]+80, screenCenter[1]+100))
        self.noButton.updatePos((screenCenter[0]-80, screenCenter[1]+100))
        self.changeButton.updatePos((screenCenter[0], screenCenter[1]-137))

    def draw(self, screen):
        self.background.draw(screen)
        self.yesButton.draw(screen)
        self.noButton.draw(screen)
        self.changeButton.draw(screen)