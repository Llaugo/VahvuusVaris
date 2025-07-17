import pygame
import room
import const
import playerClass
import picture
import text
import random
import time

# A floor is a nxn  matrix of rooms.
class Floor():
    # n: size of the floor
    def __init__(self, n, floorNumber, moveButtons):
        self.pos = (0,0)
        self.rooms: list[list[room.Room]] = [[None]*n for _ in range(n)]
        self.half = n // 2
        self.rooms[self.half][self.half] = room.Room(random.choice(const.startLayouts))
        self.currentLocation = (self.half,self.half) # Player's current room coords (start from the middle)
        self.currentRoom: room.Room = self.rooms[self.half][self.half] # Player's current room
        self.player = playerClass.Player(moveButtons, (const.worldWidth/2,const.worldHeight/2)) # Player initialization
        self.frame = picture.Picture("images/frame.png", (710,710), (0,0)) # Frame image for game area
        self.timer = const.floorTime # Timer
        self.timerText = text.Text(const.mGameFont, time.strftime('%M:%S',time.gmtime(self.timer)),(0,0))   # Timer
        self.floorText = text.Text(const.mGameFont, f'Kerros {floorNumber}', (0,0)) # Floor number
        self.birdsEye = pygame.Surface((self.currentRoom.background.get_width(), self.currentRoom.background.get_height())).convert() # multiple rooms view
        self.birdsEyeLevel = 0
        self.timeStop = False
        # Four doors from the current room out [down, right, up, left]
        self.doors = [pygame.Rect(0, 0, const.tileSize, const.tileSize),
                      pygame.Rect(0, 0, const.tileSize, const.tileSize),
                      pygame.Rect(0, 0, const.tileSize, const.tileSize),
                      pygame.Rect(0, 0, const.tileSize, const.tileSize)]

    def addStone(self):
        self.currentRoom.addStone(self.player.rect.center)

    def cleanWater(self):
        self.currentRoom.cleanWater(self.player)

    # Draw the current birdseye view
    def setBirdsEye(self, lvl):
        self.birdsEyeLevel = lvl
        if lvl > 0:
            frac = 1.0/self.birdsEyeLevel
            half = self.birdsEyeLevel//2
            for i in range(self.birdsEyeLevel):
                for j in range(self.birdsEyeLevel):
                    room = self.getRoom(self.currentLocation[0]+i-half, self.currentLocation[1]+j-half)
                    if room:
                        roomPic = room.background.copy()
                        roomPic = pygame.transform.rotozoom(room.background,0,frac).convert()
                    else:
                        roomPic = pygame.Surface((len(self.currentRoom.layout)*const.tileSize*frac, len(self.currentRoom.layout)*const.tileSize*frac)).convert()
                    self.birdsEye.blit(roomPic,(i*roomPic.get_width(),j*roomPic.get_height()))
            # Draw player picture in the correct location
            self.birdsEye.blit(self.player.image, (len(self.currentRoom.layout)*const.tileSize*half*frac + self.player.pos.x*frac - self.player.image.get_width() // 2 - self.currentRoom.rect.left*frac, len(self.currentRoom.layout)*const.tileSize*half*frac + self.player.pos.y*frac - self.player.image.get_height() - self.currentRoom.rect.top*frac))

    def stopTime(self):
        self.timeStop = not self.timeStop

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
            newRoom = room.Room(random.choice(const.roomLayouts), distFromMiddle)
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
        
    # Update floor
    def update(self):
        for i, door in enumerate(self.doors): # Detect going through doors 
            if door.colliderect(self.player.rect):
                self.nextRoom(i, self.player)
        if not self.timeStop:
            if not self.birdsEyeLevel:
                self.player.update(self.currentRoom)
            self.currentRoom.update()
            self.timer -= 1/60

    # update the position current room and the doors
    def updatePos(self, screenCenter, screenMove=(0,0)):
        self.pos = screenCenter
        self.currentRoom.updatePos(screenCenter, screenMove)
        self.player.updatePos(screenMove)
        self.frame.updatePos(screenCenter)
        self.timerText.updatePos((screenCenter[0]-141,screenCenter[1]-341))
        self.floorText.updatePos((screenCenter[0]+46,screenCenter[1]-341))
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
            self.player.draw(screen)