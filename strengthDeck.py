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
    def __init__(self, cards):
        self.pos = (0,0)
        self.shinePhase = 0
        overlaySpriteSheet = pygame.image.load('images/card_overlay.png').convert() # Load strength spritesheet
        self.overlaySprite = spriteSheet.SpriteSheet(overlaySpriteSheet)
        self.cards = cards
        self.overlays: list[tuple[pygame.Surface, pygame.Rect]] = []  # List of overlays and their rects associated with the cards
        for i in range(len(self.cards)): # create overlay for every card
            overlay = self.overlaySprite.getImage(0,250,350,const.scale/2)
            rect = overlay.get_rect()
            self.overlays.append((overlay,rect))
        self.activateButton = button.Button(12,0,(0,0), const.scale, const.gameFont(19), "Aktivoi\nkortti")
        self.background: pygame.Surface = None # Background to blit every card image

    # Update position of the cards on the screen
    def updatePos(self, pos):
        self.pos = pos
        for i, card in enumerate(self.cards): # Blit every card image and its overlay to background
            cardPos = (pos[0]-((i+1)%2)*150-165, pos[1]+((math.floor(i/2)-2)*200)+125)
            newRect = self.overlays[i][0].get_rect(topleft = cardPos)
            self.overlays[i] = (self.overlays[i][0], newRect)
        self.updateOverlays(pos)
        self.activateButton.updatePos((pos[0]+const.tileSize*15+280, pos[1]))


    def updateOverlays(self, pos):
        self.background = pygame.Surface((abs(pos[0]),pos[1]*2)).convert_alpha()
        self.background.fill((0, 0, 0, 0)) # Initialize background
        for i, overlay in enumerate(self.overlays): # Blit every card image and its overlay to background
            self.background.blit(self.cards[i].image, overlay[1])


    # Update all the cards
    def update(self, floor):
        cardReady = False
        for i, card in enumerate(self.cards): 
            if card.ready:
                if self.activateButton.pressComplete:
                    card.tryActivate(floor)
                elif card.auraDist:
                    floor.player.changeAura(card.auraDist)
                    cardReady = True
            oldCooldownN = round((card.cooldownMax - card.cooldown)/card.cooldownMax*16) + 9
            oldTimerN = round(card.timer/10) % 4 + 5
            card.update(floor) # Update cards
            cooldownN = cooldownN = round((card.cooldownMax - card.cooldown)/card.cooldownMax*16) + 9
            timerN = round(card.timer/10) % 4 + 5
            if cooldownN != oldCooldownN:
                newImg = self.overlaySprite.getImage(cooldownN,250,350,const.scale/2)
                self.overlays[i] = (newImg, self.overlays[i][1])
                self.updateOverlays(self.pos)
            elif timerN != oldTimerN:
                newImg = self.overlaySprite.getImage(timerN,250,350,const.scale/2)
                self.overlays[i] = (newImg, self.overlays[i][1])
                self.updateOverlays(self.pos)
        if not cardReady:
            floor.player.changeAura(0)

    # Reset all card actions
    def reset(self, floor):
        for card in self.cards:
            card.reset(floor)

    # Handle all button events
    def handleCards(self, event, screenSize):
        self.activateButton.handleEvent(event, screenSize)
        for i, overlay in enumerate(self.overlays):
            if event.type == pygame.FINGERDOWN and not self.cards[i].cooldown:
                if overlay[1].collidePoint(event.x*screenSize[0], event.y*screenSize[1]):
                    self.overlays[i] = (self.overlaySprite.getImage(1,250,350,const.scale/2), overlay[1])
                    self.cards[i].press()
                    self.updateOverlays(self.pos)
                elif not self.activateButton.pressComplete:
                    self.overlays[i] = (self.overlaySprite.getImage(0,250,350,const.scale/2), overlay[1])
                    self.cards[i].unpress()
                    self.updateOverlays(self.pos)
            # Track mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.cards[i].cooldown:
                if overlay[1].collidepoint(event.pos):
                    self.overlays[i] = (self.overlaySprite.getImage(1,250,350,const.scale/2), overlay[1])
                    self.cards[i].press()
                    self.updateOverlays(self.pos)
                elif not self.activateButton.pressComplete:
                    self.overlays[i] = (self.overlaySprite.getImage(0,250,350,const.scale/2), overlay[1])
                    self.cards[i].unpress()
                    self.updateOverlays(self.pos)

    # Draw the cards/background and buttons on the screen
    def draw(self, screen):
        screen.blit(self.background, (0,0))
        oldShine = round(self.shinePhase)
        self.shinePhase = (self.shinePhase + 0.1)
        for i, overlay in enumerate(self.overlays):
            if self.cards[i].ready and oldShine != round(self.shinePhase):
                newImg = self.overlaySprite.getImage(round(self.shinePhase) % 4+1,250,350,const.scale/2)
                self.overlays[i] = (newImg, self.overlays[i][1])
                self.updateOverlays(self.pos)
            screen.blit(overlay[0], overlay[1])
        for card in self.cards:
            if card.ready:
                self.activateButton.draw(screen)
                break
        
        