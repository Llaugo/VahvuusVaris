import pygame
import picture
import text
import const
import button
import shoppingList


class TradeMenu():
    def __init__(self, list: shoppingList.ShoppingList, cart, pos):
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
        #self.pos = (0,0)
        self.background = picture.Picture("images/trade_view.png", (710,710), (0,0))
        self.infoText = text.Text(const.gameFont(46), "Vahvistetaanko kauppa?",(0,0))
        self.oldItem = text.Text(const.gameFont(40), f"- {self.listItem}", (0,0), (255,0,0))
        self.newItem = text.Text(const.gameFont(40), f"+ {self.cart.item.name}", (0,0), (0,255,0))
        self.yesButton = button.Button(10,1,(0,0),const.scale, const.gameFont(23), "KYLLÄ")
        self.noButton = button.Button(12,1,(0,0),const.scale, const.gameFont(23), "EI")
        self.background.blitOnto(self.infoText.surfaces[0], (-self.infoText.surfaces[0].get_width()/2,-200), True)
        self.background.blitOnto(self.oldItem.surfaces[0], (-self.oldItem.surfaces[0].get_width()/2,-100), True)
        self.background.blitOnto(self.newItem.surfaces[0], (-self.newItem.surfaces[0].get_width()/2,-50), True)
        self.updatePos(pos)

    def confirmTrade(self):
        oldItem = self.cart.switchItem(self.listItem)
        self.list.receiveItem(oldItem.name)
        self.list.loseItem(self.itemI)

    def handleButtons(self, event, screenSize):
        self.yesButton.handleEvent(event, screenSize)
        self.noButton.handleEvent(event, screenSize)

    def updatePos(self, screenCenter):
        self.background.updatePos(screenCenter)
        self.yesButton.updatePos((screenCenter[0]+80, screenCenter[1]+100))
        self.noButton.updatePos((screenCenter[0]-80, screenCenter[1]+100))

    def draw(self, screen):
        self.background.draw(screen)
        self.yesButton.draw(screen)
        self.noButton.draw(screen)