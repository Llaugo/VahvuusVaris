import pygame
import const
import strengthCard
import picture
import button
import text
import random

# Class for the menu where the strength cards can be looked at and selected
class StrengthMenu():
    def __init__(self):
        self.pos = (0,0)
        self.background = None
        self.decks: list[list[tuple[strengthCard.StrengthCard,pygame.Rect]]] = [] # every card in categorized lists
        for i in range(26):
            if i == 0 or i == 5 or i == 10 or i == 14 or i == 17 or i == 21:
                self.decks.append([])
            card = strengthCard.createStrengthCard(i)
            rect = card.image.get_rect(center = (0,0))
            self.decks[-1].append((card,rect))
        self.favorites = []
        self.cardPiles = []
        for i in range(6):
            self.cardPiles.append(picture.Picture("images/card_pile.png",(246,386), (0,0), 0.45))
        self.titles = [text.Text(const.gameFont(15), "Viisaus ja tieto", (0,0)),
                       text.Text(const.gameFont(15), "Rohkeus", (0,0)),
                       text.Text(const.gameFont(15), "Inhimillisyys", (0,0)),
                       text.Text(const.gameFont(15), "Oikeudenmukaisuus", (0,0)),
                       text.Text(const.gameFont(15), "Kohtuullisuus", (0,0)),
                       text.Text(const.gameFont(15), "Henkisyys", (0,0))]
        self.inspectPile = 0
        self.strengthBackground = picture.Picture("images/strength_menu.png", (2500,1500), (0,0), 0.45)
        self.otter = picture.Picture("images/otter_1.png", (140,195), (0,0), 0.45)
        self.randomizeFavo()
        self.backButton = button.Button(0,4,(0,0), 0.45, const.gameFont(13), "Takaisin päävalikkoon")
        self.randomizeButton = button.Button(0,4,(0,0), 0.45, const.gameFont(15), "Arvo vahvuudet")
        self.readyButton = button.Button(0,4,(0,0), 0.45, const.gameFont(15), "Aloita seikkailu!")
        self.buttons = [self.backButton,self.randomizeButton,self.readyButton]

    def getDeck(self):
        return [self.favorites[0],self.favorites[1],self.favorites[2],self.favorites[3],self.favorites[4],self.favorites[5]]
    
    def randomizeFavo(self):
        self.favorites = []
        for i in range(len(self.decks)):
            self.favorites.append(random.choice(self.decks[i])[0])
        self.updateBackground()

    # Update menu element positions
    def updatePos(self, screenCenter):
        self.pos = screenCenter
        self.strengthBackground.updatePos(screenCenter)
        self.backButton.updatePos(((screenCenter[0]-450,screenCenter[1]+295)))
        self.randomizeButton.updatePos(((screenCenter[0],screenCenter[1]+295)))
        self.readyButton.updatePos(((screenCenter[0]+450,screenCenter[1]+295)))
        for i, pile in enumerate(self.cardPiles):
            pile.updatePos((screenCenter[0]+i*112.5-100, screenCenter[1]-187 + (i%2)*14))
        for deck in self.decks:
            for i, card in enumerate(deck):
                card[1].center = (screenCenter[0]-123+i*149, screenCenter[1]+38) 
        self.updateTextPos()
        self.updateBackground()

    def updateTextPos(self):
        for i, text in enumerate(self.titles):
            text.updatePos((self.pos[0]+i*112.5-100, self.pos[1]-283 + (i%2)*210), True)
        self.titles[self.inspectPile].updatePos((self.pos[0]+175, self.pos[1]-53), True)

    def updateBackground(self):
        self.background = pygame.Surface((2500,1500)).convert_alpha()
        self.background.fill((0, 0, 0, 0)) # Initialize background
        self.background.blit(self.strengthBackground.image,(0,0))
        for i, pile in enumerate(self.cardPiles):   # Blit all the decks
            if i != self.inspectPile:               # Except the open deck
                self.background.blit(pile.image, (408+i*112.5, 65 + (i%2)*14))
                smallPic = pygame.transform.rotozoom(self.favorites[i].image,0,0.88)
                self.background.blit(smallPic, (408+i*112.5, 86 + (i%2)*14))  # Blit chosen card on the deck
        for i, card in enumerate(self.decks[self.inspectPile]): # Blit open deck
            self.background.blit(card[0].image, (card[1].x-self.strengthBackground.rect.x,card[1].y-self.strengthBackground.rect.top))
            if card[0].imageNum == self.favorites[self.inspectPile].imageNum: # Blit otter below the selected card
                self.background.blit(self.otter.image, (408 + i*149, 440))

    # Draw menu elements on the screen
    def draw(self, screen):
        screen.blit(self.background, (self.pos[0]-1250*0.45,self.pos[1]-750*0.45))
        self.backButton.draw(screen)
        self.randomizeButton.draw(screen)
        self.readyButton.draw(screen)
        for i, text in enumerate(self.titles):
            text.draw(screen)

    # Handle button and card pressing
    def handleEvent(self, event, screenSize):
        for btn in self.buttons:
            btn.handleEvent(event, screenSize)
        # Selecting decks
        for i, pile in enumerate(self.cardPiles):
            if event.type == pygame.FINGERDOWN:
                if pile.rect.collidePoint(event.x*screenSize[0], event.y*screenSize[1]):
                    self.inspectPile = i
                    self.updateBackground()
                    self.updateTextPos()
            # Track mouse
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pile.rect.collidepoint(event.pos):
                    self.inspectPile = i
                    self.updateBackground()
                    self.updateTextPos()
        # Selecting cards
        for card in self.decks[self.inspectPile]:
            if event.type == pygame.FINGERDOWN:
                if card[1].collidePoint(event.x*screenSize[0], event.y*screenSize[1]):
                    self.favorites[self.inspectPile] = card[0]
                    self.updateBackground()
            # Track mouse
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if card[1].collidepoint(event.pos):
                    self.favorites[self.inspectPile] = card[0]
                    self.updateBackground()