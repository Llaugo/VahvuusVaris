import pygame
import const
import strengthCard
import button
import spriteSheet
import math

# Class for storing the strength cards and handling their actions
class StrengthDeck():
    # cards: list of strength cards
    # font: font used by the deck to show texts
    # lang: language of the game
    def __init__(self, cards, lang):
        self.pos = (0,0)
        self.lang = lang
        self.shinePhase = 0
        overlaySpriteSheet = pygame.image.load('images/card_overlay.png').convert() # Load strength spritesheet
        self.overlaySprite = spriteSheet.SpriteSheet(overlaySpriteSheet)
        self.cards = cards
        self.overlays: list[tuple[pygame.Surface, pygame.Rect]] = []  # List of overlays and their rects associated with the cards
        for i,card in enumerate(self.cards): # create overlay for every card
            overlay = self.overlaySprite.getImage(0,250,350,const.scale/2)
            rect = overlay.get_rect()
            self.overlays.append((overlay,rect))
        self.activateButton = button.Button(12,0,(0,0), const.scale, const.gameFont(19), const.phrase[self.lang][8])
        self.background: pygame.Surface = None # Background to blit every card image

    # Update position of the cards on the screen
    def updatePos(self, pos):
        self.pos = pos
        for i, overlay in enumerate(self.overlays): # Blit every card image and its overlay to background
            cardPos = (pos[0]-((i+1)%2)*150-165, pos[1]+((math.floor(i/2)-2)*200)+125)
            newRect = overlay[0].get_rect(topleft = cardPos)
            self.overlays[i] = (overlay[0], newRect)
        self.updateImages(pos)
        self.activateButton.updatePos((pos[0]+const.tileSize*15+280, pos[1]))

    # Construct the background image of all the cards
    def updateImages(self, pos):
        self.background = pygame.Surface((abs(pos[0]),pos[1]*2)).convert_alpha() # Reset background surface/image
        self.background.fill((0, 0, 0, 0)) # Initialize background
        for i, overlay in enumerate(self.overlays): # Blit every card image to background
            self.background.blit(self.cards[i].image, overlay[1])

    # Update all the cards
    def update(self, floor):
        cardReady = False
        card4 = self.cards[4]
        for i, card in enumerate(self.cards): 
            if card.ready:
                if self.activateButton.pressComplete:
                    card.tryActivate(floor)
                    self.overlays[i] = (self.overlaySprite.getImage(0,250,350,const.scale/2), self.overlays[i][1])
                    self.updateImages(self.pos)
                elif card.auraDist:
                    floor.player.changeAura(card.auraDist)
                    cardReady = True
            oldCooldownN = math.floor((card.cooldownMax - card.cooldown)/card.cooldownMax*16) + 9
            oldTimerN = math.floor(card.timer/10) % 4 + 5
            if card4.imageNum == 19 and card4.timer and i != 4: # If prudence is on, update only cooldown timers
                if not card.timer:
                    card.updateCooldown()
                    if card4.level == 3 and card4.timer%2: # If prudence is on level 3, every other tick doubles the cooldown reduce
                        card.updateCooldown()
            else:
                card.update(floor) # Update cards
            cooldownN = cooldownN = math.floor((card.cooldownMax - card.cooldown)/card.cooldownMax*16) + 9
            timerN = math.floor(card.timer/10) % 4 + 5
            if cooldownN != oldCooldownN:
                newImg = self.overlaySprite.getImage(cooldownN,250,350,const.scale/2)
                self.overlays[i] = (newImg, self.overlays[i][1])
            elif timerN != oldTimerN and card.imageNum != 22:
                newImg = self.overlaySprite.getImage(timerN,250,350,const.scale/2)
                self.overlays[i] = (newImg, self.overlays[i][1])
        if not cardReady:
            floor.player.changeAura(0)

    # Reset all card actions
    def reset(self, floor):
        for i,card in enumerate(self.cards):
            card.reset(floor)
            self.overlays[i] = (self.overlaySprite.getImage(0,250,350,const.scale/2), self.overlays[i][1])

    # Handle all button events
    def handleCards(self, event, screenSize):
        self.activateButton.handleEvent(event, screenSize)
        for i, overlay in enumerate(self.overlays):
            if event.type == pygame.FINGERDOWN and not self.cards[i].cooldown:
                if overlay[1].collidePoint(event.x*screenSize[0], event.y*screenSize[1]):
                    self.overlays[i] = (self.overlaySprite.getImage(1,250,350,const.scale/2), overlay[1])
                    self.cards[i].press()
                    if self.cards[i].imageNum == 11: self.updateImages(self.pos)
                elif not self.activateButton.pressComplete:
                    self.overlays[i] = (self.overlaySprite.getImage(0,250,350,const.scale/2), overlay[1])
                    self.cards[i].unpress()
                    if self.cards[i].imageNum == 11: self.updateImages(self.pos)
            # Track mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.cards[i].cooldown:
                if overlay[1].collidepoint(event.pos):
                    self.overlays[i] = (self.overlaySprite.getImage(1,250,350,const.scale/2), overlay[1])
                    self.cards[i].press()
                    if self.cards[i].imageNum == 11: self.updateImages(self.pos)
                elif not self.activateButton.pressComplete:
                    self.overlays[i] = (self.overlaySprite.getImage(0,250,350,const.scale/2), overlay[1])
                    self.cards[i].unpress()
                    if self.cards[i].imageNum == 11: self.updateImages(self.pos)

    # Draw the cards/background and buttons on the screen
    def draw(self, screen):
        screen.blit(self.background, (0,0))
        oldShine = math.floor(self.shinePhase)
        self.shinePhase = (self.shinePhase + 0.1)
        for i, overlay in enumerate(self.overlays):
            if self.cards[i].ready and oldShine != math.floor(self.shinePhase):
                newImg = self.overlaySprite.getImage(math.floor(self.shinePhase) % 4+1,250,350,const.scale/2)
                self.overlays[i] = (newImg, self.overlays[i][1])
            screen.blit(overlay[0], overlay[1])
        for card in self.cards:
            if card.ready:
                self.activateButton.draw(screen)
                break

    def saveDeck(self):
        deckArr = []
        for card in self.cards:
            deckArr.append(card.imageNum)
        for card in self.cards:
            deckArr.append(card.level)
        for card in self.cards:
            deckArr.append(card.auraDist)
        for card in self.cards:
            deckArr.append(card.timerMax)
        for card in self.cards:
            deckArr.append(card.cooldownMax)
        for card in self.cards:
            if card.imageNum == 6: 
                deckArr.append(card.swimSpeed)
            elif card.imageNum == 11:
                while len(deckArr) < 31: deckArr.append(None)
                deckArr.append(card.battery)
            elif card.imageNum == 23 or card.imageNum == 25:
                while len(deckArr) < 32: deckArr.append(None)
                deckArr.append(card.litWidth)
        return deckArr

        
# deckArr: [6x card numbers, 6x card levels, 6x auraDist, 6x timerMax, 6x cooldownMax, 3x extra values]
def deckLoader(deckArr, lang):
    cards = []
    for i in range(6):
        card = strengthCard.createStrengthCard(deckArr[i])
        card.level = deckArr[6+i]
        card.auraDist = deckArr[12+i]
        card.timerMax = deckArr[18+i]
        card.cooldownMax = deckArr[24+i]
        if card.imageNum == 6: 
            card.swimSpeed = deckArr[30]
        if card.imageNum == 11:
            card.battery = deckArr[31]
            card.batteryReset = math.floor(card.level)
        if card.imageNum == 23 or card.imageNum == 25:
            card.litWidth = deckArr[32]
        cards.append(card)
    return StrengthDeck(cards,lang)