import pygame
import const
import strengthCard
import button
import math

# Class for storing the strength cards and handling their actions
class StrengthDeck():
    # cards: list of integers corresponding to the wanted strengths' numbers
    # font: font used by the deck to show texts
    def __init__(self, cards, font):
        self.cards: list[strengthCard.StrengthCard] = [] # List of strength cards
        self.buttons: list[button.Button] = []  # List of buttons associated with the cards
        for i in cards: # Create strengthcards according to the given numbers
            self.cards.append(strengthCard.createStrengthCard(i))
        for i in range(len(self.cards)): # create buttons for every card
            self.buttons.append(button.Button(12,(0,0), const.scale/2, font, "Aktivoi"))
        self.background: pygame.Surface = None # Background to blit every card image

    # Update position of the cards on the screen
    def updatePos(self, pos):
        self.background = pygame.Surface((pos[0],pos[1]*2)).convert_alpha()
        self.background.fill((0, 0, 0, 0)) # Initialize background
        for i, card in enumerate(self.cards): # Blit every card image to background
            self.background.blit(card.image, (pos[0]-((i+1)%2)*150-175, pos[1]+((math.floor(i/2)-2)*220)+125))
            self.buttons[i].updatePos((pos[0]-((i+1)%2)*150-145, pos[1]+((math.floor(i/2)-2)*220)+320)) # update button positions

    # Update all the cards
    def update(self, player, room):
        for i, btn in enumerate(self.buttons): 
            if btn.activeFinger: # Activate cards when button is pressed
                self.cards[i].tryActivate(player,room)
            self.cards[i].update(player,room) # Update cards

    # Reset all card actions
    def reset(self, player, room):
        for card in self.cards:
            card.reset(player, room)

    # Handle all button events
    def handleButtons(self, event, screenSize):
        for btn in self.buttons:
            btn.handleEvent(event, screenSize)
    
    # Draw the cards/background and buttons on the screen
    def draw(self, screen):
        screen.blit(self.background, (0,0))
        for btn in self.buttons:
            btn.draw(screen)
        