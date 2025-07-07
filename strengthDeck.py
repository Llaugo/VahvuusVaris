import pygame
import const
import strengthCard
import button
import math

class StrengthDeck():
    def __init__(self, cards, font):
        self.pos = (0,0)
        self.cards: list[strengthCard.StrengthCard] = []
        self.buttons: list[button.Button] = []
        for i in cards:
            self.cards.append(strengthCard.createStrengthCard(i))
        for i in range(len(self.cards)):
            self.buttons.append(button.Button(12,(0,0), const.scale/2, font, "Aktivoi"))
        self.background: pygame.Surface = None

    def updatePos(self, pos):
        self.background = pygame.Surface((pos[0],pos[1]*2)).convert_alpha()
        self.background.fill((0, 0, 0, 0))
        for i, card in enumerate(self.cards):
            self.background.blit(card.image, (pos[0]-((i+1)%2)*150-175, pos[1]+((math.floor(i/2)-2)*220)+125))
            self.buttons[i].updatePos((pos[0]-((i+1)%2)*150-145, pos[1]+((math.floor(i/2)-2)*220)+320))

    def update(self, player, room):
        for i, btn in enumerate(self.buttons):
            if btn.activeFinger:
                self.cards[i].tryActivate(player,room)
            self.cards[i].update(player,room)

    def reset(self, player, room):
        for card in self.cards:
            card.reset(player, room)

    def handleButtons(self, event, screenSize):
        for btn in self.buttons:
            btn.handleEvent(event,screenSize)
            
    def draw(self, screen):
        screen.blit(self.background, self.pos)
        for btn in self.buttons:
            btn.draw(screen)
        