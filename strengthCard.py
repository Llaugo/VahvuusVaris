import pygame
import const
import spriteSheet

class StrengthCard():
    # imageNum: the index of the card image
    def __init__(self, imageNum):
        cardSpriteSheet = pygame.image.load('images/strength_sheet.png').convert() # Load strength spritesheet
        self.cardSprite = spriteSheet.SpriteSheet(cardSpriteSheet)
        self.image = self.cardSprite.getImage(imageNum,250,350,const.scale/2)
        self.timer = 0
        self.cooldown = 0
        self.timerMax = 900
        self.cooldownMax = 360

    # Activate the card and start the active timer if the card is not on cooldown
    # Returns True if activation was successful, False otherwise
    def tryActivate(self):
        if not self.cooldown:
            self.timer = self.timerMax
            self.cooldown = self.cooldownMax
            return True
        return False

    # Do card action if card is active
    def update(self):
        raise NotImplementedError("Please Implement this method")

    # update the timers of the card
    def updateTimers(self):
        if self.timer:
            self.timer -= 1
        elif self.cooldown:
            self.cooldown -= 1

    # Reset the card timers to the base state
    def reset(self):
        self.timer = 0
        self.cooldown = 0

    def isActive(self):
        if self.timer:
            return True
        return False
        
    
class ZestCard(StrengthCard):
    def __init__(self):
        super().__init__(8)

    def update(self):
        if self.timer > 0:
            const.playerSpeed = const.basePlayerSpeed*2
        else:
            const.playerSpeed = const.basePlayerSpeed
        self.updateTimers()

    def reset(self):
        super().reset()
        const.playerSpeed = const.basePlayerSpeed

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
        pass
    elif n == 19:
        pass
    elif n == 20:
        pass
    elif n == 21:
        pass
    elif n == 22:
        pass
    elif n == 23:
        pass
    else:
        return StrengthCard(0)
