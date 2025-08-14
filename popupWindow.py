import pygame
import text
import picture
import button
import const


class ConfirmWindow():
    def __init__(self, newtext, font, lang):
        self.background = picture.Picture("images/confirmWindow.png",(1000,1000),(0,0), const.scale*0.45)
        self.text = text.Text(font, newtext, (0,0), center=True)
        self.yesButton = button.Button(10,1,(0,0),const.scale, const.gameFont(23), const.phrase[lang][10])
        self.noButton = button.Button(12,1,(0,0),const.scale, const.gameFont(23), const.phrase[lang][11])

    def handleButtons(self, event, screenSize):
        self.yesButton.handleEvent(event, screenSize)
        self.noButton.handleEvent(event, screenSize)

    def updatePos(self, pos):
        self.background.updatePos(pos)
        self.text.updatePos((pos[0],pos[1]-100))
        self.yesButton.updatePos((pos[0]+80, pos[1]+100))
        self.noButton.updatePos((pos[0]-80, pos[1]+100))

    def draw(self, screen):
        self.background.draw(screen)
        self.text.draw(screen)
        self.yesButton.draw(screen)
        self.noButton.draw(screen)