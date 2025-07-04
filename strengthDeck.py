import pygame
import const
import strengthCard

class StrengthDeck():
    def __init__(self, cards: tuple[int,int,int,int,int,int], font):
        self.pos = (0,0)
        self.cards: list[strengthCard.StrengthCard] = []
        for card in cards:
            self.cards.append(strengthCard.StrengthCard(card, font))
        self.background: pygame.Surface = None

    def updatePos(self, pos):
        self.background = pygame.Surface((pos[0],pos[1]*2)).convert_alpha()
        self.background.fill((0, 0, 0, 0))
        for i, card in enumerate(self.cards):
            self.background.blit(card.image, (pos[0]-((i+1)%2)*150-175, pos[1]-((round(i/2)-2)*220)-320))
            #card.activateButton.updatePos((pos[0]-((i+1)%2)*150-145, pos[1]-((round(i/2)-2)*220)-127))
            
    def draw(self, screen):
        screen.blit(self.background, self.pos)
        #for card in self.cards:
        #    card.activateButton.draw(screen)
        