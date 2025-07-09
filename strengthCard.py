import pygame
import const
import spriteSheet
import playerClass

# Class for strength cards. There is a parent class and 26 child classes, one each strength.
# Each card gives the player some ability or boost, which has a timer during which the strength is active.
# After the ability ends, there is a cooldown for using the ability.
class StrengthCard():
    # imageNum: the index of the card image
    def __init__(self, imageNum):
        cardSpriteSheet = pygame.image.load('images/strength_sheet.png').convert() # Load strength spritesheet
        self.cardSprite = spriteSheet.SpriteSheet(cardSpriteSheet)
        self.image = self.cardSprite.getImage(imageNum,250,350,const.scale/2)
        self.timer = 0          # timer for the ability
        self.cooldown = 0       # timer for the cooldown
        self.timerMax = 300     # timer duration
        self.cooldownMax = 300  # cooldown duration

    # Activates the card and starts the active timer if the card is not on cooldown
    # Returns True if activation was successful, False otherwise
    def tryActivate(self, player, room):
        if not self.cooldown:
            self.timer = self.timerMax
            self.cooldown = self.cooldownMax
            return True
        return False

    # Do card action if card is active
    def update(self, player, room):
        self.updateTimers()

    # update the timers of the card
    def updateTimers(self):
        if self.timer:          # Update timer if timer is active
            self.timer -= 1
        elif self.cooldown:     # Update cooldown timer if cooldown is active
            self.cooldown -= 1

    # Reset the card timers to the base state
    def reset(self, player, room):
        self.timer = 0
        self.cooldown = 0

    # Returns True if timer is on, False if not
    def isActive(self):
        if self.timer:
            return True
        return False

# Zest card gives the player a speed boost
class ZestCard(StrengthCard):
    def __init__(self):
        super().__init__(8)

    # Change players speed if not on cooldown
    def tryActivate(self, player, room):
        if super().tryActivate(player, room):
            player.changeSpeed(const.basePlayerSpeed*1.5, self.timerMax)

    # Reset player speed to normal
    def reset(self, player, room):
        super().reset(player, room)
        player.resetSpeed()

# Humility card makes the player smaller to fit through small spaces
class HumilityCard(StrengthCard):
    def __init__(self):
        super().__init__(18)

    # Make player smaller if cooldown is not on
    def tryActivate(self, player: playerClass.Player, room):
        if super().tryActivate(player, room):
            player.toggleSize(room, 0.5)

    # Turn player size back to normal if timer is out
    def update(self, player: playerClass.Player, room):
        if self.timer == 1:
            player.toggleSize(room)
        self.updateTimers()

    # Reset size to normal
    def reset(self, player: playerClass.Player, room):
        super().reset(player, room)
        player.toggleSize(room)

# Gratitude card can drop stones on the ground, to keep track of steps and gives a speed boost when walking over the stones
class GratitudeCard(StrengthCard):
    def __init__(self):
        super().__init__(22)
        self.timerMax = 60 # This card's timer means how long the speedboost lasts

    # Adds a stone to the ground if not on cooldown
    def tryActivate(self, player, room):
        if not self.cooldown:
            room.addStone(player.rect.center)
            self.cooldown = self.cooldownMax            

    # Fill boost timer if player is standing on a stone
    def update(self, player, room):
        for stn in room.stones:
            if player.rect.colliderect(stn[1]): # Check collision with all the stones
                self.timer = self.timerMax
                player.changeSpeed(const.basePlayerSpeed*1.5, self.timerMax) # change speed upon collision
                break
        # Update both timers
        if self.timer:
            self.timer -= 1
        if self.cooldown:
            self.cooldown -= 1
    
    # Reset player speed to normal
    def reset(self, player, room):
        super().reset(player, room)
        player.resetSpeed()


# Return a strength card respective to the given integer.
def createStrengthCard(n):
    if n == 0:
        pass
    elif n == 1:
        pass
    elif n == 2:
        pass
    elif n == 3:
        pass
    elif n == 4:
        pass
    elif n == 5:
        pass
    elif n == 6:
        pass
    elif n == 7:
        pass
    elif n == 8:
        return ZestCard()
    elif n == 9:
        pass
    elif n == 10:
        pass
    elif n == 11:
        pass
    elif n == 12:
        pass
    elif n == 13:
        pass
    elif n == 14:
        pass
    elif n == 15:
        pass
    elif n == 16:
        pass
    elif n == 17:
        pass
    elif n == 18:
        return HumilityCard()
    elif n == 19:
        pass
    elif n == 20:
        pass
    elif n == 21:
        pass
    elif n == 22:
        return GratitudeCard()
    elif n == 23:
        pass
    else:
        return StrengthCard(0)
