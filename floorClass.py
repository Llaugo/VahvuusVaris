import pygame
import room
import const
import playerClass
import picture
import text
import shoppingList
import button
import random
import time

# A floor is a nxn  matrix of rooms.
class Floor():
    # n: size of the floor
    # lang: language of the game
    def __init__(self, n, floorNumber, moveButtons, shoppinglist, lang):
        self.pos = (0,0)
        self.lang = lang
        self.rooms: list[list[room.Room]] = [[None]*n for _ in range(n)]
        self.half = n // 2
        #self.rooms[self.half][self.half] = room.Room(random.choice(const.startLayouts), self.lang)
        self.rooms[self.half][self.half] = room.Room(random.choice(const.testRoom), self.lang) # FOR TESTING
        self.currentLocation = (self.half,self.half) # Player's current room coords (start from the middle)
        self.currentRoom: room.Room = self.rooms[self.half][self.half] # Player's current room
        self.player = playerClass.Player(moveButtons, (const.worldWidth/2,const.worldHeight/2)) # Player initialization
        self.shoppinglist = shoppinglist
        self.frame = picture.Picture("images/frame.png", (710,710), (0,0)) # Frame image for game area
        self.timer = const.floorTime # Timer
        self.timerText = text.Text(const.gameFont(32), time.strftime('%M:%S',time.gmtime(self.timer)),(0,0))   # Timer
        self.floorText = text.Text(const.gameFont(32), f'{const.phrase[self.lang][2]} {floorNumber}', (0,0)) # Floor number
        self.itemButton = button.Button(14,1,(0,0),const.scale, const.gameFont(23), const.phrase[self.lang][4], (130,63,0)) # Button to pick up items
        self.birdsEye = pygame.Surface((self.currentRoom.background.get_width(), self.currentRoom.background.get_height())).convert() # multiple rooms view
        self.birdsEyeLevel = 0
        self.timeStop = False
        self.advertBlock = False
        # Four doors from the current room out [down, right, up, left]
        self.doors = [pygame.Rect(0, 0, const.tileSize, const.tileSize),
                      pygame.Rect(0, 0, const.tileSize, const.tileSize),
                      pygame.Rect(0, 0, const.tileSize, const.tileSize),
                      pygame.Rect(0, 0, const.tileSize, const.tileSize)]

    def breakBox(self, dist):
        if not self.currentRoom.breakBox(self.player, dist):
            self.player.speak(const.phrase[self.lang][46])

    def addStone(self):
        self.currentRoom.addStone(self.player.rect.center)

    def addItem(self):
        if not self.currentRoom.addItem():
            self.player.speak(const.phrase[self.lang][56])

    def showItemNames(self, bool):
        self.currentRoom.showItemNames(bool)

    def changeDarkness(self, radius, duration, clear=False):
        if not self.currentRoom.changeDarkness(radius, duration, clear):
            self.player.speak(const.phrase[self.lang][47])

    def cleanWater(self, dist):
        if not self.currentRoom.cleanWater(self.player, dist):
            self.player.speak(const.phrase[self.lang][55])

    # Draw the current birdseye view
    def setBirdsEye(self, lvl):
        self.birdsEyeLevel = lvl
        if lvl > 0:
            frac = 1.0/self.birdsEyeLevel
            half = self.birdsEyeLevel//2
            for i in range(self.birdsEyeLevel):
                for j in range(self.birdsEyeLevel):
                    room = self.getRoom(self.currentLocation[0]+i-half, self.currentLocation[1]+j-half)
                    if room and not room.darkness:
                        roomPic = room.background.copy()
                        roomPic = pygame.transform.rotozoom(room.background,0,frac).convert()
                    else:
                        roomPic = pygame.Surface((len(self.currentRoom.layout)*const.tileSize*frac, len(self.currentRoom.layout)*const.tileSize*frac)).convert()
                    self.birdsEye.blit(roomPic,(i*roomPic.get_width(),j*roomPic.get_height()))
            # Draw player picture in the correct location
            self.birdsEye.blit(self.player.image, (len(self.currentRoom.layout)*const.tileSize*half*frac + self.player.pos.x*frac - self.player.image.get_width() // 2 - self.currentRoom.rect.left*frac, len(self.currentRoom.layout)*const.tileSize*half*frac + self.player.pos.y*frac - self.player.image.get_height() - self.currentRoom.rect.top*frac))

    def stopTime(self):
        self.timeStop = not self.timeStop

    def advertBlockStart(self):
        self.advertBlock = True

    def advertBlockEnd(self):
        self.advertBlock = False

    # Rotates nearby adverts
    def rotateAdverts(self, dist):
        zone = pygame.Rect(0,0,dist,dist)
        zone.center = self.player.rect.center
        rotated = False
        for add in self.currentRoom.adverts:
            if add.rect.colliderect(zone):
                add.rotate(1)
                rotated = True
        if rotated:
            self.currentRoom.updatePos(self.pos,(0,0))
            self.currentRoom.reconstruct()
        else:
            self.player.speak(const.phrase[self.lang][48])

    def destroyAdvert(self, dist):
        if not self.currentRoom.destroyAdvert(self.player, dist):
            self.player.speak(const.phrase[self.lang][48])

    def swapPlayer(self):
        if not self.currentRoom.swapPlayer(self.player):
            self.player.speak(const.phrase[self.lang][51])

    def showCartOwners(self, timer):
        self.currentRoom.showCartOwners(True, timer)

    def tradeWithNpc(self):
        ans = self.currentRoom.tradeWithNpc(self.shoppinglist)
        if ans == -1:
            self.player.speak(const.phrase[self.lang][52])
        elif ans == 0:
            self.player.speak(const.phrase[self.lang][54])
        elif ans == 1:
            self.player.speak(const.phrase[self.lang][53])

    def askCartPushing(self, timer):
        ans = self.currentRoom.askCartPushing(timer)
        if ans == -1:
            self.player.speak(const.phrase[self.lang][52])
        elif ans == 0:
            self.player.speak(const.phrase[self.lang][53])

    def leadCartPushing(self):
        ans = self.currentRoom.leadCartPushing()
        if ans == -1:
            self.player.speak(const.phrase[self.lang][52])
        elif ans == 0:
            self.player.speak(const.phrase[self.lang][53])
        elif ans == 1:
            self.player.speak(const.phrase[self.lang][57])

    def resetCartOwnerView(self):
        self.currentRoom.resetCartOwnerView()

    def findLove(self):
        if self.currentRoom.talkNpc:
            self.player.speak(const.phrase[self.lang][58])
            return True
        else:
            self.player.speak(const.phrase[self.lang][52])
            return False

    # Go to next room in the given direction
    # dir: direction of the next room (0=d,1=r,2=u,3=l)
    def nextRoom(self, dir, player):
        if dir == 0:
            self.currentLocation = (self.currentLocation[0], self.currentLocation[1] + 1)
            player.resetRect((self.pos[0]+5, self.pos[1]-const.tileSize*6-30))
        elif dir == 1:
            self.currentLocation = (self.currentLocation[0] + 1, self.currentLocation[1])
            player.resetRect((self.pos[0]-const.tileSize*7+5, self.pos[1]+10))
        elif dir == 2:
            self.currentLocation = (self.currentLocation[0], self.currentLocation[1] - 1)
            player.resetRect((self.pos[0]+5, self.pos[1]+const.tileSize*6+50))
        else:
            self.currentLocation = (self.currentLocation[0] - 1, self.currentLocation[1])
            player.resetRect((self.pos[0]+const.tileSize*7+5, self.pos[1]+10))
        # get the correct room or create one if not generated
        newRoom = self.getRoom(self.currentLocation[0],self.currentLocation[1])
        # Transfer the state of darkness
        newRoom.litRadius = self.currentRoom.litRadius
        newRoom.lightDuration = self.currentRoom.lightDuration
        self.currentRoom.litRadius = 0
        self.currentRoom.lightDuration = 0
        self.currentRoom = newRoom

    # Get a room from memory or create one if not yet generated
    def getRoom(self,x,y):
        if len(self.rooms) <= x or len(self.rooms) <= y or x < 0 or y < 0:
            return None
        if self.rooms[x][y]:
            newRoom = self.rooms[x][y]
        else:
            distFromMiddle = abs(x - self.half) + abs(y - self.half)
            newRoom = room.Room(random.choice(const.roomLayouts), self.lang, distFromMiddle)
            self.rooms[x][y] = newRoom
            # Delete doors that would out of index
            if x == 0:
                newRoom.removeDoor(0)
            elif x == len(self.rooms)-1:
                newRoom.removeDoor(2)
            if y == 0:
                newRoom.removeDoor(1)
            elif y == len(self.rooms)-1:
                newRoom.removeDoor(3)
            newRoom.updatePos(self.pos)
        return newRoom
    
    def handleButtons(self, event, screenSize):
        self.itemButton.handleEvent(event, screenSize)
        if self.currentRoom.tradeView:
            self.currentRoom.tradeView.handleButtons(event, screenSize)
        
    # Update floor
    def update(self):
        for i, door in enumerate(self.doors): # Detect going through doors 
            if door.colliderect(self.player.rect):
                self.nextRoom(i, self.player)
        if not self.timeStop:
            if not self.birdsEyeLevel:
                if not self.currentRoom.tradeView:
                    self.player.update(self.currentRoom)
                else:
                    if self.currentRoom.tradeView.yesButton.pressComplete:
                        self.currentRoom.tradeView.confirmTrade()
                        self.currentRoom.deleteTradeView()
                    elif self.currentRoom.tradeView.noButton.pressComplete:
                        self.currentRoom.deleteTradeView()
                if not self.advertBlock:
                    for add in self.currentRoom.adverts:
                        add.update(self.player, self.currentRoom)
            self.currentRoom.update(self.player)
            self.timer -= 1/60
            
    # update the position current room and the doors
    def updatePos(self, newScreenSize, screenCenter, screenMove=(0,0)):
        self.pos = screenCenter
        self.currentRoom.updatePos(screenCenter, screenMove)
        self.player.updatePos(screenMove)
        self.shoppinglist.updatePos((newScreenSize[0] - self.currentRoom.rect.left/2, newScreenSize[1]/4))
        self.frame.updatePos(screenCenter)
        self.timerText.updatePos((screenCenter[0]-143,screenCenter[1]-341))
        self.floorText.updatePos((screenCenter[0]+46,screenCenter[1]-341))
        self.itemButton.updatePos((self.currentRoom.rect.right+180,newScreenSize[1]/2))
        self.doors[0].center = (screenCenter[0], screenCenter[1] + const.tileSize*8)
        self.doors[1].center = (screenCenter[0] + const.tileSize*8, screenCenter[1])
        self.doors[2].center = (screenCenter[0], screenCenter[1] - const.tileSize*8+10)
        self.doors[3].center = (screenCenter[0] - const.tileSize*8, screenCenter[1])

    def draw(self, screen):
        if self.birdsEyeLevel:
            screen.blit(self.birdsEye, self.currentRoom.rect)
        else:
            self.currentRoom.draw(screen, self.player)
        self.frame.draw(screen)
        self.timerText.draw(screen,time.strftime('%M:%S', time.gmtime(self.timer)))
        self.floorText.draw(screen)
        if not self.birdsEyeLevel:
            playerDrawn = False
            for npc in self.currentRoom.npcs: # Draw player in front of the npc if it's lower down
                if not playerDrawn and npc.pos.y+2 > self.player.pos.y:
                    self.player.draw(screen)
                    playerDrawn = True
                npc.draw(screen)
            if not playerDrawn:
                self.player.draw(screen)
        if self.currentRoom.tradeView:
            self.currentRoom.tradeView.draw(screen)
        self.shoppinglist.draw(screen)
        # Picking up items from the room
        if not self.currentRoom.tradeView:
            for item in self.currentRoom.items:
                if item.rect.colliderect(self.player.rect):  # Show the button if player is on top of the item
                    self.itemButton.draw(screen)
                    if self.itemButton.pressComplete:         # Take item if button is active
                        self.itemButton.unpress()
                        self.shoppinglist.receiveItem(item.name)
                        self.currentRoom.removeItem(item)