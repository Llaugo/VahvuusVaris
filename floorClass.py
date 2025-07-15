import pygame
import room
import const
import random

# A floor is a nxn  matrix of rooms.
class Floor():
    # n: size of the floor
    def __init__(self, n):
        self.pos = (0,0)
        self.rooms: list[list[room.Room]] = [[None]*n for _ in range(n)]
        self.half = n // 2
        self.rooms[self.half][self.half] = room.Room(random.choice(const.startLayouts))
        '''
        for i in range(n):
            self.rooms.append([])
            for j in range(n):
                if i == j == half:
                    self.rooms[i].append(room.Room(random.choice(const.startLayouts)))
                else:
                    self.rooms[i].append(room.Room(random.choice(const.roomLayouts), abs(i - half) + abs(j - half)))
        '''
        self.currentLocation = (self.half,self.half) # Player's current room coords (start from the middle)
        self.currentRoom: room.Room = self.rooms[self.half][self.half] # Player's current room
        # Four doors from the current room out [down, right, up, left]
        self.doors = [pygame.Rect(0, 0, const.tileSize, const.tileSize),
                      pygame.Rect(0, 0, const.tileSize, const.tileSize),
                      pygame.Rect(0, 0, const.tileSize, const.tileSize),
                      pygame.Rect(0, 0, const.tileSize, const.tileSize)]

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
        if self.rooms[self.currentLocation[0]][self.currentLocation[1]]:
            newRoom = self.rooms[self.currentLocation[0]][self.currentLocation[1]]
        else:
            newRoom = room.Room(random.choice(const.roomLayouts), abs(self.currentLocation[0] - self.half) + abs(self.currentLocation[1] - self.half))
            self.rooms[self.currentLocation[0]][self.currentLocation[1]] = newRoom
            # Delete doors that would out of index
            if self.currentLocation[0] == 0:
                newRoom.removeDoor(0)
            elif self.currentLocation[0] == len(self.rooms)-1:
                newRoom.removeDoor(2)
            if self.currentLocation[1] == 0:
                newRoom.removeDoor(1)
            elif self.currentLocation[1] == len(self.rooms)-1:
                newRoom.removeDoor(3)
            newRoom.updatePos(self.pos)
        # Transfer the state of darkness
        newRoom.litRadius = self.currentRoom.litRadius
        newRoom.lightDuration = self.currentRoom.lightDuration
        self.currentRoom.litRadius = 0
        self.currentRoom.lightDuration = 0
        self.currentRoom = newRoom
        
    # Update floor
    def update(self, player):
        for i, door in enumerate(self.doors): # Detect going through doors 
            if door.colliderect(player.rect):
                self.nextRoom(i,player)
        self.currentRoom.update()

    # update the position current room and the doors
    def updatePos(self, screenCenter, screenMove=(0,0)):
        self.pos = screenCenter
        self.currentRoom.updatePos(screenCenter, screenMove)
        self.doors[0].center = (screenCenter[0], screenCenter[1] + const.tileSize*8)
        self.doors[1].center = (screenCenter[0] + const.tileSize*8, screenCenter[1])
        self.doors[2].center = (screenCenter[0], screenCenter[1] - const.tileSize*8+10)
        self.doors[3].center = (screenCenter[0] - const.tileSize*8, screenCenter[1])

    def draw(self, screen, player):
        self.currentRoom.draw(screen, player)