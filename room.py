import pygame
import const
import tile
import item
import text
import random

# A class for rooms which consist of tiles in a grid.
class Room():
    # layout: the tile layout in the room
    # pos: position of the room
    # roomDistance: How far away the room/item is from the middle. Far away rooms produce more rarer items.
    def __init__(self, layout, roomDistance=0):
        self.layout: list[list[tile.Tile]] = [] # Matrix of every tile
        self.pos = (0,0)                        # Room center
        self.roomDistance = roomDistance
        self.exit = None                        # Does the room have an exit
        self.initialize(layout)                 # Initialize room's tiles
        self.tiles = [x for xs in self.layout for x in xs] # All the room's tiles in a list
        self.background = pygame.Surface((len(layout[0])*const.tileSize, len(layout)*const.tileSize)).convert() # Room background surface
        self.rect = self.background.get_rect(center = self.pos)
        self.solidRects = []                    # walls and solid objects of the room
        self.items = []                         # items in the room
        self.showItemNames = False              # If True, item names are shown
        self.stones = []                        # stones in the room (list[(image,rect)])
        for i,row in enumerate(self.layout):    # Blit all the tiles to a single background image
            for j,oneTile in enumerate(row):
                self.background.blit(oneTile.image, (j*const.tileSize, i*const.tileSize))
        self.darkness = None                    # None if room is dark
        self.litRadius = 0                      # Extra light space around the player in the dark
        self.lightDuration = 0                  # Duration of light space
        # Chance for setting the room as dark if the room isn't a lift
        if len(layout) > 5 and random.random() < const.darknessProbability and roomDistance != 0:
            self.darkness = pygame.Surface(((len(layout[0])-2)*const.tileSize, (len(layout)-2)*const.tileSize), flags=pygame.SRCALPHA) # dark square
            self.darkness.fill((0, 0, 0, 255))  # Fill with black
        self.updatePos(self.pos,(0,0))          # Set positions correctly

    # Update room
    def update(self):
        self.lightDuration = max(self.lightDuration-1, 0) # update light duration timer
        if not self.lightDuration: # Reset lights when timer runs out
            self.resetLights()

    # Update room position
    # screenCenter: center of the screen
    # how much the screen size (x,y) has been changed
    def updatePos(self, screenCenter, screenMove=(0,0)):
        self.pos = screenCenter
        self.rect = self.background.get_rect(center = self.pos)
        halfLength = round((len(self.layout)-1)/2)  # Helper value
        self.solidRects: list[pygame.Rect] = []     # Reset solids
        self.items: list[item.Item] = []            # Reset items
        for i, row in enumerate(self.layout):       # Update all tile positions
            for j, tile in enumerate(row):
                tilePos = (screenCenter[0]+(j-halfLength)*const.tileSize, screenCenter[1]+(i-halfLength)*const.tileSize)
                tile.updatePos(tilePos)             # Update tile
                if tile.solid:                      # Update solid walls
                    newRect = pygame.Rect(i*const.tileSize, j*const.tileSize, const.tileSize, const.tileSize)
                    newRect.center = tilePos
                    self.solidRects.append(newRect)
                elif tile.tileType == 5:            # Update crate tiles
                    newRect = pygame.Rect(i*const.tileSize, j*const.tileSize, 23, 25)
                    newRect.center = (tilePos[0]+5, tilePos[1]+5)
                    self.solidRects.append(newRect)
                if tile.item:                       # Update items
                    self.items.append(tile.item)
        random.shuffle(self.items)
        self.itemNamesTitle.updatePos((self.rect.left + 5, self.rect.top + 45))
        for i, itm in enumerate(self.items): # List of items, if needed for showing room items
            itm.text.updatePos((self.rect.left + 5, self.rect.top + 75 + i*itm.text.surfaces[0].get_height() + itm.text.lineSpacing))
        for stn in self.stones:
            stn[1].center = (stn[1].centerx + screenMove[0]/2, stn[1].centery + screenMove[1]/2)

    # Remove item from the rooms memory
    # item: the item to be removed
    def removeItem(self, item: item.Item):
        self.items.remove(item)         # Remove from the room
        for row in self.layout:
            for tile in row:
                if tile.item == item:   # And remove from the tile's memory
                    tile.deleteItem()

    # Add a stone to the room
    def addStone(self, pos):
        image = pygame.image.load('images/stone.png').convert_alpha() # Get image
        rect = image.get_rect(center = pos) # Get rect
        self.stones.append((image, rect))

    # Turn on item name showing
    def revealItems(self):
        self.showItemNames = True

    # Turn off item name showing
    def hideItems(self):
        self.showItemNames = False

    # Add one item randomly into the room
    def addItem(self, rarity=1):
        freeTiles = []
        for tile in self.tiles: # Check all free shelves
            if tile.isShelf() and not tile.item:
                freeTiles.append(tile)
        if freeTiles:
            rndTile = random.choice(freeTiles)
            rndTile.addItem(self.roomDistance)  # Add an item to a random tile
            self.items.append(rndTile.item)     # Add the item to room
            random.shuffle(self.items)
            for i, itm in enumerate(self.items): # List of items, if needed for showing room items
                itm.text.updatePos((self.rect.left + 5, self.rect.top + 75 + i*itm.text.surfaces[0].get_height() + itm.text.lineSpacing))
    
    # Lighten up a dark room
    # radius: radius of the lit area, negative numbers create a beam of light in front of the player
    # duration: duration of the light being on
    # clear: if True, get rid of darkness altogether
    def changeDarkness(self, radius, duration, clear=False):
        if clear:
            self.darkness = None
            self.litRadius = 0
            self.lightDuration = 0
        elif duration > self.lightDuration:
            self.litRadius = radius
            self.lightDuration = duration

    # Reset the lit area around the player
    def resetLights(self):
        self.litRadius = 0
        self.lightDuration = 0

    # Draw each tile, item and stone in this room
    def draw(self, screen, player):
        screen.blit(self.background, self.rect) # background
        for item in self.items:                 # items
            item.draw(screen)
        for stn in self.stones:                 # stones
            screen.blit(stn[0],stn[1])
        # Fill with darkness
        if self.darkness:
            self.darkness.fill((0, 0, 0, 255))
            playerPos = (player.rect.centerx-self.rect.left-const.tileSize, player.rect.centery-3-self.rect.top-const.tileSize)
            if self.litRadius >= 0: # Create a circle of light
                for a,r in [(200,18+self.litRadius), (150,16+self.litRadius), (100,14+self.litRadius), (50,12+self.litRadius), (0,10+self.litRadius)]:
                    pygame.draw.circle(self.darkness, (0, 0, 0, a), playerPos, r)
            else: # Create a beam of light
                if player.facing % 2 == 0:
                    for a,r in [(200,8-self.litRadius),(150,6-self.litRadius),(100,4-self.litRadius),(50,2-self.litRadius),(0,-self.litRadius)]:
                        pygame.draw.circle(self.darkness, (0, 0, 0, a), playerPos, r/2)
                        pygame.draw.line(self.darkness, (0,0,0,a), [playerPos[0], playerPos[1]], [playerPos[0], playerPos[1] + (1 - player.facing)*700], r)
                else:
                    for a,r in [(200,8-self.litRadius),(150,6-self.litRadius),(100,4-self.litRadius),(50,2-self.litRadius),(0,-self.litRadius)]:
                        pygame.draw.circle(self.darkness, (0, 0, 0, a), playerPos, r/2)
                        pygame.draw.line(self.darkness, (0,0,0,a), [playerPos[0], playerPos[1]], [playerPos[0] + (2 - player.facing)*700, playerPos[1]], r)
            screen.blit(self.darkness, (self.rect.left+const.tileSize,self.rect.top+const.tileSize))
        # Show item name list
        if self.showItemNames:
            self.itemNamesTitle.draw(screen)
        for item in self.items:
            if self.showItemNames:              # Show item names if True
                item.text.draw(screen)
    
    # Construct the room tiles from the given layout
    # Only use once upon creation
    # layout: the number matrix of the room's layout
    def initialize(self, layout):
        lift = (len(layout) <= 5) # The layout represents a lift
        # Create the correct tile by the number
        for i,row in enumerate(layout):
            self.layout.append([])
            for j,c in enumerate(row):
                if c == 0: # Wall
                    if lift: # Lift has special walls
                        self.layout[i].append(tile.Tile(16, (0,0), const.scale))
                    else:
                        self.layout[i].append(tile.Tile(6, (0,0), const.scale))
                elif c == 1 or c == 7: # Floor
                    if lift: # Lift has special floor
                        self.layout[i].append(tile.Tile(4, (0,0), const.scale))
                    else:
                        self.layout[i].append(tile.Tile(random.randint(1,3), (0,0), const.scale))
                elif c == 2: # Shelf
                    self.layout[i].append(tile.Tile(random.randint(7,15), (0,0), const.scale, self.roomDistance))
                elif c == 3: # Exit
                    self.exit = tile.Tile(0, (0,0), const.scale)
                    self.layout[i].append(self.exit)
                elif c == 4: # crate
                    self.layout[i].append(tile.Tile(5, (0,0), const.scale))
                else:
                    raise ValueError(f'The room layout contains unknown value: {c}')
        # Set the neighbours for the tiles
        for i, row in enumerate(self.layout):
            for j, c in enumerate(row):
                if j: # Set the tile on top as neighbour if this isn't the top tile
                    self.layout[i][j-1].setNeighbour(0,c)
                if i: # Set the previous tile as neighbour if this isn't the first tile
                    self.layout[i-1][j].setNeighbour(1,c)
        # Set the title for the item names list
        self.itemNamesTitle = text.Text(const.mGameFont,"Huoneessa olevat esineet:",(0,0),(25, 28, 54))
