import pygame
import const
import strengthCard

class StrengthDeck():
    def __init__(self, cards: tuple[int,int,int,int,int,int]):
        self.pos = (0,0)
        self.cards: list[strengthCard.StrengthCard] = []
        for card in cards:
            self.cards.append(strengthCard.StrengthCard(card))
        self.background: pygame.Surface = None

    def updatePos(self, pos):
        self.background = pygame.Surface((pos[0],pos[1])).convert_alpha()
        self.background.fill((0, 0, 0, 0))
        self.background.blit(self.cards[0].image, (pos[0]*2/7-125/2, pos[1]*1/6-175/2))
        self.background.blit(self.cards[1].image, (pos[0]*2/7-125/2, pos[1]*3/6-175/2))
        self.background.blit(self.cards[2].image, (pos[0]*2/7-125/2, pos[1]*5/6-175/2))
        self.background.blit(self.cards[3].image, (pos[0]*5/7-125/2, pos[1]*1/6-175/2))
        self.background.blit(self.cards[4].image, (pos[0]*5/7-125/2, pos[1]*3/6-175/2))
        self.background.blit(self.cards[5].image, (pos[0]*5/7-125/2, pos[1]*5/6-175/2))
            
    def draw(self, screen):
        screen.blit(self.background, self.pos)
        