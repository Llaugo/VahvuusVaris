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
        self.imageNum = imageNum
        cardSpriteSheet = pygame.image.load('images/strength_sheet.png').convert() # Load strength spritesheet
        self.cardSprite = spriteSheet.SpriteSheet(cardSpriteSheet)
        self.image = self.cardSprite.getImage(imageNum,250,350,const.scale/2)
        self.ready = False
        self.auraDist = 0
        self.timer = 0          # timer for the ability
        self.cooldown = 0       # timer for the cooldown
        self.timerMax = 300     # timer duration
        self.cooldownMax = 300  # cooldown duration

    # Activates the card and starts the active timer if the card is not on cooldown
    # Returns True if activation was successful, False otherwise
    def tryActivate(self, floor):
        if not self.cooldown:
            self.timer = self.timerMax
            self.cooldown = self.cooldownMax
            self.unpress()
            return True
        return False

    # Do card action if card is active
    def update(self, floor):
        self.updateTimers()

    # update the timers of the card
    def updateTimers(self):
        if self.timer:          # Update timer if timer is active
            self.timer -= 1
        elif self.cooldown:     # Update cooldown timer if cooldown is active
            self.cooldown -= 1

    # Reset the card timers to the base state
    def reset(self, floor):
        self.timer = 0
        self.cooldown = 0

    # Returns True if timer is on, False if not
    def isActive(self):
        if self.timer:
            return True
        return False
    
    def press(self):
        self.ready = True
    def unpress(self):
        self.ready = False

class CreativityCard(StrengthCard):
    def __init__(self):
        super().__init__(0)
# Curiosity card breaks open boxes that are in the way
class CuriosityCard(StrengthCard):
    def __init__(self):
        super().__init__(1)
        self.timer = 1
        self.auraDist = 80

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.breakBox(self.auraDist)

# Judgement cards shows what items there are in the room
class JudgementCard(StrengthCard):
    def __init__(self):
        super().__init__(2)

    # Show the item names in the room if not on cooldown
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            self.timer = self.timerMax
            floor.showItemNames(True)

    # Hide item names, if timer ends
    def update(self, floor):
        if self.timer == 1:
            floor.showItemNames(False)
        self.updateTimers()

    # Reset timers and hide item names
    def reset(self, floor):
        super().reset(floor)
        floor.showItemNames(False)

# Learning card gets rid of darkness in the dark rooms
class LearningCard(StrengthCard):
    def __init__(self):
        super().__init__(3)

    # Makes the visible area around the player wider if in a dark room
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.currentRoom.changeDarkness(0, 0, True)

# Perspective card shows the rooms around the current room
class PerspectiveCard(StrengthCard):
    def __init__(self):
        super().__init__(4)

    # Show rooms around the current room if not on cooldown
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.setBirdsEye(3)

    # Set view to normal when the timer ends
    def update(self, floor):
        if self.timer == 1:
            floor.setBirdsEye(0)
        self.updateTimers()

    # Reset view to normal
    def reset(self, floor):
        super().reset(floor)
        floor.setBirdsEye(0)

# Bravery card makes the player able to push heavier carts
class BraveryCard(StrengthCard):
    def __init__(self):
        super().__init__(5)

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.player.changeStrength(8)

    def update(self, floor):
        if self.timer == 1:
            floor.player.changeStrength(const.basePlayerStrength)
        self.updateTimers()

    def reset(self, floor):
        super().reset(floor)
        floor.player.changeStrength(const.basePlayerStrength)

# Perseverance card makes player to be able to walk through water
class PerseveranceCard(StrengthCard):
    def __init__(self):
        super().__init__(6)

    # Change player swimming speed if not on cooldown
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.player.swim(const.basePlayerSpeed*0.25, self.timerMax)

    # Reset player swimming speed to normal (off)
    def reset(self, floor):
        super().reset(floor)
        floor.player.resetSwim()

# Honesty card rotates the adverts
class HonestyCard(StrengthCard):
    def __init__(self):
        super().__init__(7)
        self.auraDist = const.tileSize*2

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.rotateAdverts(self.auraDist)
    
# Zest card gives the player a speed boost
class ZestCard(StrengthCard):
    def __init__(self):
        super().__init__(8)

    # Change players speed if not on cooldown
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.player.changeSpeed(const.basePlayerSpeed*1.5, self.timerMax)

    # Reset player speed to normal
    def reset(self, floor):
        super().reset(floor)
        floor.player.resetSpeed()

# Grit card destroys advert in front of the player
class GritCard(StrengthCard):
    def __init__(self):
        super().__init__(9)
        self.auraDist = 100

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.destroyAdvert(self.auraDist)

# Kindness card makes it possible to move through/past npcs
class KindnessCard(StrengthCard):
    def __init__(self):
        super().__init__(10)

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.player.setNpcCollitionTimer(self.timerMax)

    def reset(self, floor):
        floor.player.setNpcCollitionTimer(0)
        super().reset(floor)

class LoveCard(StrengthCard):
    def __init__(self):
        super().__init__(11)

# Shows the cart-npc pairs
class SocialCard(StrengthCard):
    def __init__(self):
        super().__init__(12)

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.showCartOwners(True)

    def update(self, floor):
        if self.timer == 1:
            floor.showCartOwners(False)
        self.updateTimers()

    def reset(self, floor):
        floor.showCartOwners(False)
        super().reset(floor)

# Compassion card swaps the player with an npc
class CompassionCard(StrengthCard):
    def __init__(self):
        super().__init__(13)
        self.timerMax = 1

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.swapPlayer()

class FairnessCard(StrengthCard):
    def __init__(self):
        super().__init__(14)

class LeadershipCard(StrengthCard):
    def __init__(self):
        super().__init__(15)

class TeamworkCard(StrengthCard):
    def __init__(self):
        super().__init__(16)

# Forgiveness card cleans nearby waters
class ForgivenessCard(StrengthCard):
    def __init__(self):
        super().__init__(17)
        self.auraDist = const.tileSize

    # Clean nearby water from the room if not on cooldown
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.cleanWater(self.auraDist)

# Humility card makes the player smaller to fit through small spaces
class HumilityCard(StrengthCard):
    def __init__(self):
        super().__init__(18)

    # Make player smaller if cooldown is not on
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.player.toggleSize(floor.currentRoom, 0.5)

    # Turn player size back to normal if timer is out
    def update(self, floor):
        if self.timer == 1:
            floor.player.toggleSize(floor.currentRoom)
        self.updateTimers()

    # Reset size to normal
    def reset(self, floor):
        super().reset(floor)
        floor.player.toggleSize(floor.currentRoom)

# Prudence card stops the time
class PrudenceCard(StrengthCard):
    def __init__(self):
        super().__init__(19)

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.stopTime()

    def update(self, floor):
        if self.timer == 1:
            floor.stopTime()
        self.updateTimers()
    
    def reset(self, floor):
        super().reset(floor)
        floor.stopTime()

# Regulation card stop the pushing of the advert screens
class RegulationCard(StrengthCard):
    def __init__(self):
        super().__init__(20)

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.advertBlockStart()

    def update(self, floor):
        if self.timer == 1:
            floor.advertBlockEnd()
        self.updateTimers()

    def reset(self,floor):
        super().reset(floor)
        floor.advertBlockEnd()

# Appreciation card makes a new item appear somewhere in the room
class AppreciationCard(StrengthCard):
    def __init__(self):
        super().__init__(21)
        self.timerMax = 1

    # Adds an item to room if not on cooldown
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.currentRoom.addItem()

# Gratitude card can drop stones on the ground, to keep track of steps and gives a speed boost when walking over the stones
class GratitudeCard(StrengthCard):
    def __init__(self):
        super().__init__(22)
        self.timerMax = 60 # This card's timer means how long the speedboost lasts

    # Adds a stone to the ground if not on cooldown
    def tryActivate(self, floor):
        if not self.cooldown:
            floor.addStone()
            self.cooldown = self.cooldownMax
            self.unpress()

    # Fill boost timer if player is standing on a stone
    def update(self, floor):
        for stn in floor.currentRoom.stones:
            if floor.player.rect.colliderect(stn[1]): # Check collision with all the stones
                self.timer = self.timerMax
                floor.player.changeSpeed(const.basePlayerSpeed*1.3, self.timerMax) # change speed upon collision
                break
        # Update both timers
        if self.timer:
            self.timer -= 1
        if self.cooldown:
            self.cooldown -= 1
    
    # Reset player speed to normal
    def reset(self, floor):
        super().reset(floor)
        floor.player.resetSpeed()

# Hope card makes makes a long visible area in front of the player in the dark rooms
class HopeCard(StrengthCard):
    def __init__(self):
        super().__init__(23)

    # Makes the visible beam in front of the player if in a dark room
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.currentRoom.changeDarkness(-50, self.timerMax)

    # Reset visible area and timers
    def reset(self, floor):
        super().reset(floor)
        floor.currentRoom.resetLights()

# Humor card makes player to be able to swim through water
class HumorCard(StrengthCard):
    def __init__(self):
        super().__init__(24)

    # Change player swimming speed if not on cooldown
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.player.swim(const.basePlayerSpeed*0.5, self.timerMax)

    # Reset player swimming speed to normal (off)
    def reset(self, floor):
        super().reset(floor)
        floor.player.resetSwim()

# Spirituality card makes the visible area around the player wider in the dark rooms
class SpiritualityCard(StrengthCard):
    def __init__(self):
        super().__init__(25)

    # Makes the visible area around the player wider if in a dark room
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.currentRoom.changeDarkness(70, self.timerMax)

    # Reset visible area and timers
    def reset(self, floor):
        super().reset(floor)
        floor.currentRoom.resetLights()
    

# Return a strength card respective to the given integer.
def createStrengthCard(n):
    if n == 0:
        return CreativityCard()
    elif n == 1:
        return CuriosityCard()
    elif n == 2:
        return JudgementCard()
    elif n == 3:
        return LearningCard()
    elif n == 4:
        return PerspectiveCard()
    elif n == 5:
        return BraveryCard()
    elif n == 6:
        return PerseveranceCard()
    elif n == 7:
        return HonestyCard()
    elif n == 8:
        return ZestCard()
    elif n == 9:
        return GritCard()
    elif n == 10:
        return KindnessCard()
    elif n == 11:
        return LoveCard()
    elif n == 12:
        return SocialCard()
    elif n == 13:
        return CompassionCard()
    elif n == 14:
        return FairnessCard()
    elif n == 15:
        return LeadershipCard()
    elif n == 16:
        return TeamworkCard()
    elif n == 17:
        return ForgivenessCard()
    elif n == 18:
        return HumilityCard()
    elif n == 19:
        return PrudenceCard()
    elif n == 20:
        return RegulationCard()
    elif n == 21:
        return AppreciationCard()
    elif n == 22:
        return GratitudeCard()
    elif n == 23:
        return HopeCard()
    elif n == 24:
        return HumorCard()
    elif n == 25:
        return SpiritualityCard()
    else:
        return StrengthCard(n)
