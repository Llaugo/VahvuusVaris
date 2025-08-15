import pygame
import text
import picture
import button
import const
import strengthDeck
import shoppingList
import time


class EndScreen():
    def __init__(self, deck, shoplist, screenCenter, lang):
        self.lang = lang
        self.deck: strengthDeck.StrengthDeck = deck
        self.shoplist: shoppingList.ShoppingList = shoplist
        self.timerText = text.Text(const.gameFont(35), "-00:00",(0,0))   # Timer
        self.floorText = text.Text(const.gameFont(35), 'No floors', (0,0)) # Floor number
        self.maintext = text.Text(const.gameFont(60), "Main text", (0,0))
        self.subtext = text.Text(const.gameFont(35), "more text", (0,0))
        self.readyButton = button.Button(0,4,(0,0),const.scale, const.gameFont(28), const.phrase[self.lang][12])
        self.active = False
        self.pos = screenCenter

    def activate(self, timer=300, floorNumber=1):
        if not self.active:
            self.timerText.setText(time.strftime(f'{const.phrase[self.lang][66]} %M:%S',time.gmtime(timer)))
            self.floorText.setText(f'{const.phrase[self.lang][2]} {floorNumber}')
            self.active = True
            self.updatePos(self.pos)
            return True
        return False

    def deactivate(self):
        self.active = False

    def handleButtons(self, event, screenSize):
        self.readyButton.handleEvent(event, screenSize)

    def updatePos(self, pos):
        self.pos = pos
        if self.active:
            if self.deck:
                self.deck.updatePos((pos[0]/2, pos[1]))
            if self.shoplist:
                self.shoplist.updatePos((pos[0], pos[1]))
            self.floorText.updatePos((pos[0]+160, pos[1]-30))
            self.timerText.updatePos((pos[0]+160, pos[1]+30))
            self.maintext.updatePos((pos[0]*4/8,pos[1]*1/7))
            self.subtext.updatePos((pos[0]*4/8,pos[1]*3/9))
            self.readyButton.updatePos((pos[0], pos[1]*7/4))

    def draw(self, screen):
        if self.deck:
            self.deck.draw(screen)
        if self.shoplist:
            self.shoplist.draw(screen)
        self.floorText.draw(screen)
        self.timerText.draw(screen)
        self.maintext.draw(screen)
        self.subtext.draw(screen)
        self.readyButton.draw(screen)


class WinScreen(EndScreen):
    def __init__(self, deck, shoplist, screenCenter, lang):
        super().__init__(deck, shoplist, screenCenter, lang)
        self.maintext = text.Text(const.gameFont(60), const.phrase[lang][62], (0,0), (0,194,0))
        self.subtext = text.Text(const.gameFont(35), const.phrase[lang][63], (0,0), (0,102,0))

class LoseScreen(EndScreen):
    def __init__(self, deck, shoplist, screenCenter, lang):
        super().__init__(deck, shoplist, screenCenter, lang)
        self.maintext = text.Text(const.gameFont(60), const.phrase[lang][64], (0,0), (194,0,0))
        self.subtext = text.Text(const.gameFont(35), const.phrase[lang][65], (0,0), (102,0,0))

class PrologueScreen(EndScreen):
    def __init__(self, deck, shoplist, screenCenter, lang):
        super().__init__(deck, shoplist, screenCenter, lang)
        self.maintext = text.Text(const.gameFont(60), const.phrase[lang][67], (0,0), (0,0,194))
        self.subtext = text.Text(const.gameFont(35), const.phrase[lang][68], (0,0), (0,0,102))
        self.readyButton = button.Button(0,4,(0,0),const.scale, const.gameFont(28), const.phrase[self.lang][14])