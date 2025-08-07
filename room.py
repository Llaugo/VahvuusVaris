import pygame
import const
import tile
import item
import text
import cart
import npc
import tradeMenu
import random

# A class for rooms which consist of tiles in a grid.
class Room():
    # layout: the tile layout in the room
    # pos: position of the room
    # lang: language of the game
    # roomDistance: How far away the room/item is from the middle. Far away rooms produce more rarer items.
    def __init__(self, layout, lang, roomDistance=0):
        self.lang = lang
        self.layout: list[list[tile.Tile]] = [] # Matrix of every tile
        self.pos = (0,0)                        # Room center
        self.roomDistance = roomDistance
        self.exit = None                        # Does the room have an exit
        self.carts = []                         # carts in the room
        self.npcs = []                          # npcs in the room
        self.npcCartPairs = []                  # pairs of npcs and carts
        self.pushableCarts = []                 # carts that can be pushed
        self.talkNpc = None                     # The npc the player is currently interacting with
        self.initialize(layout)                 # Initialize room's tiles
        self.tiles = [x for xs in self.layout for x in xs] # All the room's tiles in a list
        self.background = pygame.Surface((len(layout[0])*const.tileSize, len(layout)*const.tileSize)).convert() # Room background surface
        self.rect = self.background.get_rect(center = self.pos)
        self.reconstruct()                      # Blit all the tiles to a single background image
        self.solidRects = []                    # walls and solid objects of the room
        self.waterRects = []                    # watertiles in the room
        self.items = []                         # items in the room
        self.itemNamesTitle = text.Text(const.gameFont(32), const.phrase[self.lang][6],(0,0),(25, 28, 54)) # Title for the item names list
        self.adverts = []                       # adverts in the room
        self.itemNameView = False               # If True, item names are shown
        self.cartOwnerView = None               # If not specified, show all carts
        self.cartOwnerDuration = 0              # How long to show carts for
        self.tradeView = None                   # If True, show trading buttons
        self.stones = []                        # stones in the room (list[(image,rect)])
        self.darkness = None                    # None if room is dark
        self.owners = pygame.Surface(((len(self.layout[0]))*const.tileSize, (len(self.layout))*const.tileSize), flags=pygame.SRCALPHA)
        self.owners.fill((0, 0, 0, 0))
        self.litRadius = 0                      # Extra light space around the player in the dark
        self.lightDuration = 0                  # Duration of light space
        # Chance for setting the room as dark if the room isn't a lift
        if len(layout) > 5 and random.random() < const.darknessProbability and roomDistance != 0:
            self.darkness = pygame.Surface(((len(layout[0])-2)*const.tileSize, (len(layout)-2)*const.tileSize), flags=pygame.SRCALPHA) # dark square
            self.darkness.fill((0, 0, 0, 255))  # Fill with black
        #self.updatePos(self.pos,(0,0))          # Set positions correctly

    # Update room
    def update(self, player):
        self.lightDuration = max(self.lightDuration-1, 0) # update light duration timer
        if not self.lightDuration: # Reset lights when timer runs out
            self.resetLights()
        frontNpc = player.npcInFront(self)
        if self.talkNpc != frontNpc: # Change the active npc
            if self.talkNpc:
                self.talkNpc.turnBack()
            self.talkNpc = frontNpc
            if frontNpc:
                frontNpc.turn((player.facing+2)%4)
        if self.cartOwnerDuration == 1:
            self.cartOwnerView = None
        self.cartOwnerDuration = max(self.cartOwnerDuration-1, 0)
        for npc in self.npcs:
            npc.update(self, player)

    # Update room position and reset all object hitboxes
    # screenCenter: center of the screen
    # how much the screen size (x,y) has been changed
    def updatePos(self, screenCenter, screenMove=(0,0)):
        self.pos = screenCenter
        self.rect.center = self.pos
        halfLength = round((len(self.layout)-1)/2)  # Helper value
        self.solidRects: list[pygame.Rect] = []     # Reset solids
        self.waterRects: list[pygame.Rect] = []     # Reset waters
        self.items: list[item.Item] = []            # Reset items
        self.adverts = []                           # Reset adverts
        for i, row in enumerate(self.layout):       # Update all tile positions
            for j, tile in enumerate(row):
                tilePos = (screenCenter[0]+(j-halfLength)*const.tileSize, screenCenter[1]+(i-halfLength)*const.tileSize)
                tile.updatePos(tilePos)             # Update tile
                if tile.solid:                      # Update solid walls
                    newRect = pygame.Rect(i*const.tileSize, j*const.tileSize, const.tileSize, const.tileSize)
                    newRect.center = tilePos
                    if tile.isWater():
                        self.waterRects.append(newRect)
                    else:
                        self.solidRects.append(newRect)
                elif tile.tileType == 5:            # Update crate tiles
                    newRect = pygame.Rect(i*const.tileSize, j*const.tileSize, 23, 25)
                    newRect.center = (tilePos[0]+5, tilePos[1]+5)
                    self.solidRects.append(newRect)
                elif tile.hasAdvert():
                    self.adverts.append(tile.advert)
                    tile.advert.setStream(self.streamLength(j,i,tile.advert.dir))
                if tile.item:                       # Update items
                    self.items.append(tile.item)
        random.shuffle(self.items)
        self.itemNamesTitle.updatePos((self.rect.left + 5, self.rect.top + 45))
        for i, itm in enumerate(self.items): # List of items, if needed for showing room items
            itm.text.updatePos((self.rect.left + 5, self.rect.top + 75 + i*itm.text.surfaces[0].get_height() + itm.text.lineSpacing))
        for stn in self.stones:
            stn[1].center = (stn[1].centerx + screenMove[0]/2, stn[1].centery + screenMove[1]/2)
        for cart in self.carts:
            cart.updatePos(screenMove)
            self.solidRects.append(cart.rect)
        for npc in self.npcs:
            npc.updatePos(screenMove)
            #self.solidRects.append(npc.rect)
        if self.tradeView:
            self.tradeView.updatePos(screenCenter)


    # Calcuates the point where the stream ends
    def streamLength(self,tx,ty,dir):
        dx, dy = (dir%2*(dir-2)*-1, (dir-1)%2*(dir-1)*-1)
        length = 0
        x,y = tx+dx,ty+dy
        # step until we hit bounds or a solid tile
        while 0 <= y < len(self.layout) and 0 <= x < len(self.layout[0]):
            if self.layout[y][x].solid:
                break
            length += 1
            x += dx
            y += dy
        return (self.layout[ty][tx].pos[0] + dx*(length*const.tileSize + 23), self.layout[ty][tx].pos[1] + dy*(length*const.tileSize + 23))

    # Remove one entrence and make it wall
    # dir: (d=0,r=1,u=2,l=3)
    def removeDoor(self, dir):
        if dir == 0:
            self.layout[(len(self.layout)//2)][0].makeWall()
        elif dir == 1:
            self.layout[0][(len(self.layout)//2)].makeWall()
        elif dir == 2:
            self.layout[(len(self.layout)//2)][len(self.layout)-1].makeWall()
        elif dir == 3:
            self.layout[len(self.layout)-1][(len(self.layout)//2)].makeWall()
        self.reconstruct()

    def breakBox(self, player, dist):
        clearradius = pygame.Rect(0, 0, dist, dist)
        clearradius.center = player.pos
        broken = False
        for tile in self.tiles:
            if tile.rect.colliderect(clearradius):
                if tile.breakBox():
                    broken = True
        if broken:
            self.reconstruct()
            self.updatePos(self.pos)
            return True
        return False

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

    def showItemNames(self, bool):
        self.itemNameView = bool

    # Add one item randomly into the room
    # Returns True if item was added, False if no shelves to add to
    def addItem(self):
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
            return True
        return False
    
    # Lighten up a dark room
    # radius: radius of the lit area, negative numbers create a beam of light in front of the player
    # duration: duration of the light being on
    # clear: if True, get rid of darkness altogether
    # Returns True if there was darkness to be changed
    def changeDarkness(self, radius, duration, clear=False):
        if not self.darkness:
            return False
        if clear:
            self.darkness = None
            self.litRadius = 0
            self.lightDuration = 0
        elif duration > self.lightDuration:
            self.litRadius = radius
            self.lightDuration = duration
        return True

    # Reset the lit area around the player
    def resetLights(self):
        self.litRadius = 0
        self.lightDuration = 0

    # Clean the nearby tiles from water
    # Returns True if water was cleared, False if there was no water
    def cleanWater(self, player, dist):
        waterHit = False
        clearradius = pygame.Rect(0, 0, dist, dist)
        clearradius.center = player.pos
        for tile in self.tiles:
            if tile.rect.colliderect(clearradius):
                if tile.clearWater():
                    waterHit = True
        if waterHit:
            self.reconstruct()
            self.waterRects: list[pygame.Rect] = []     # Reset waters
            for i, row in enumerate(self.layout):       # Update all tile positions
                for j, tile in enumerate(row):
                    if tile.isWater():
                        newRect = pygame.Rect(i*const.tileSize, j*const.tileSize, const.tileSize, const.tileSize)
                        newRect.center = tile.pos
                        self.waterRects.append(newRect)
        return waterHit

    # Returns True if advert was destroyed
    def destroyAdvert(self, player, dist):
        advertHit = False
        clearradius = pygame.Rect(0, 0, dist, dist)
        clearradius.center = player.pos
        for tile in self.tiles:
            if tile.rect.colliderect(clearradius):
                if tile.clearAdvert():
                    advertHit = True
        if advertHit:
            self.reconstruct()
            self.adverts = [] # Reset adverts
            for i, row in enumerate(self.layout):
                for j, tile in enumerate(row):
                    if tile.hasAdvert():
                        self.adverts.append(tile.advert)
                        tile.advert.setStream(self.streamLength(j,i,tile.advert.dir))
        return advertHit

    # Returns wheather the the carts were pushed
    # pusher: entity pushing the cart, player/npc (has to have .strength and .rect)
    def collideCarts(self, pusher, dir, vel, player):
        success = True
        if not pusher.strength:
            pushCarts = self.pushableCarts
        else:
            pushCarts = self.carts
        for cart in pushCarts:
            if cart.rect.colliderect(pusher.rect):
                if not cart.push(dir, vel, self, pusher, player):
                    success = False
        return success
    
    # Switches places between the player and a possible npc in front
    # Return True if there was NPC to swap places with
    def swapPlayer(self, player):
        npc = player.npcInFront(self)
        if npc:
            if player.facing % 2 == 0:
                playerPos = ((player.rect.centerx+npc.rect.centerx)/2, player.rect.centery)
                player.resetRect(((player.rect.centerx+npc.rect.centerx)/2 + 5, npc.rect.centery + 10))
                npc.setPos((playerPos[0] + 0, playerPos[1] + 0))
            else:
                playerPos = (player.rect.centerx, (player.rect.centery+npc.rect.centery)/2)
                player.resetRect((npc.rect.centerx + 5, (player.rect.centery+npc.rect.centery)/2 + 10))
                npc.setPos((playerPos[0] + 0, playerPos[1] + 0))
            npc.turn(player.facing)
            player.facing = (player.facing + 2) % 4
            return True
        return False
    
    # bool: If True, show all the carts, otherwise show one (self.cartOwnerView)
    def showCartOwners(self, bool, timer):
        if timer > self.cartOwnerDuration:
            self.cartOwnerDuration = timer
            if bool:
                self.cartOwnerView = None

    # Returns -1 if no NPC, 0 if no items to trade, 1 if NPC has no cart, 2 if Success
    def tradeWithNpc(self, list):
        foundCart = None
        if self.talkNpc:
            npci = self.npcs.index(self.talkNpc)
            if len(self.carts) > npci:
                foundCart = self.carts[npci]
        else:
            return -1
        if foundCart:
            self.tradeView = tradeMenu.TradeMenu(list, foundCart, self.pos, self.lang)
            if self.tradeView.listItem:
                return 2
            else:
                self.deleteTradeView()
                return 0
        return 1
    
    def deleteTradeView(self):
        self.tradeView = None

    # Returns -1 if no NPC, 0 if no NPC's cart and 1 if NPC has cart
    def askCartPushing(self,timer):
        foundCart = None
        if self.talkNpc:
            npci = self.npcs.index(self.talkNpc)
            if len(self.carts) > npci:
                foundCart = self.carts[npci]
        else:
            return -1
        if foundCart:
            self.pushableCarts.append(foundCart)
            self.cartOwnerView = foundCart
            self.showCartOwners(False, timer)
            return 1
        return 0
    
    # Returns -1 if no NPC, 0 if no NPC's cart, 1 if cart obstructed and 2 if successful
    def leadCartPushing(self):
        foundCart = None
        if self.talkNpc:
            npci = self.npcs.index(self.talkNpc)
            if len(self.carts) > npci:
                foundCart = self.carts[npci]
        else:
            return -1
        if foundCart:
            cartPushPos = foundCart.pos + (37*(foundCart.dir%2)*(foundCart.dir-2), 37*((foundCart.dir-1)%2*(foundCart.dir-1)))
            if self.talkNpc.teleport(cartPushPos, self):
                self.talkNpc.turnBack(foundCart.dir)
                self.talkNpc.walk(const.npcWalkDur)
                return 2
            else:
                return 1
        return 0
    
    def resetCartOwnerView(self):
        self.cartOwnerDuration = 0

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
                if player.facing % 2 == 0: # Direction of the beam
                    for a,r in [(200,8-self.litRadius),(150,6-self.litRadius),(100,4-self.litRadius),(50,2-self.litRadius),(0,-self.litRadius)]:
                        pygame.draw.circle(self.darkness, (0, 0, 0, a), playerPos, r/2)
                        pygame.draw.line(self.darkness, (0,0,0,a), [playerPos[0], playerPos[1]], [playerPos[0], playerPos[1] + (1 - player.facing)*700], r)
                else:
                    for a,r in [(200,8-self.litRadius),(150,6-self.litRadius),(100,4-self.litRadius),(50,2-self.litRadius),(0,-self.litRadius)]:
                        pygame.draw.circle(self.darkness, (0, 0, 0, a), playerPos, r/2)
                        pygame.draw.line(self.darkness, (0,0,0,a), [playerPos[0], playerPos[1]], [playerPos[0] + (2 - player.facing)*700, playerPos[1]], r)
            screen.blit(self.darkness, (self.rect.left+const.tileSize,self.rect.top+const.tileSize))
        if self.cartOwnerDuration:
            self.owners.fill((0, 0, 0, 0))
            if not self.cartOwnerView: # Show all cart npc pairs
                for i,pair in enumerate(self.npcCartPairs):
                    npcPos = (pair[0].rect.centerx-self.rect.left, pair[0].rect.centery-self.rect.top+1)
                    cartPos = (pair[1].rect.centerx-self.rect.left, pair[1].rect.centery-self.rect.top+1)
                    pygame.draw.circle(self.owners, ((i*50)%225, (-i*50-50)%225, (i*50-100)%225, 120), npcPos, 22)
                    pygame.draw.circle(self.owners, ((i*50)%225, (-i*50-50)%225, (i*50-100)%225, 120), cartPos, 22)
                    pair[1].item.text.draw(screen)
                screen.blit(self.owners,self.rect.topleft)
                if not self.carts:
                    player.speak(const.phrase[self.lang][49])
                elif not self.npcs:
                    player.speak(const.phrase[self.lang][50])
            else:   # Show only one cart npc pair
                for i,pair in enumerate(self.npcCartPairs):
                    if self.npcCartPairs[i][1] == self.cartOwnerView:
                        npcPos = (pair[0].rect.centerx-self.rect.left, pair[0].rect.centery-self.rect.top+1)
                        cartPos = (pair[1].rect.centerx-self.rect.left, pair[1].rect.centery-self.rect.top+1)
                        pygame.draw.circle(self.owners, ((i*50)%225, (-i*50-50)%225, (i*50-100)%225, 120), npcPos, 22)
                        pygame.draw.circle(self.owners, ((i*50)%225, (-i*50-50)%225, (i*50-100)%225, 120), cartPos, 22)
                screen.blit(self.owners,self.rect.topleft)
        for cart in self.carts:
            cart.draw(screen)
        # Show item name list
        if self.itemNameView:
            self.itemNamesTitle.draw(screen)
            for item in self.items:
                item.text.draw(screen)

    # Generates the background image again from the matrix of tiles)
    # Call anytime the background image/tiles are changed
    def reconstruct(self):
        for i,row in enumerate(self.layout):    # Blit tile images to background 
            for j,oneTile in enumerate(row):
                self.background.blit(oneTile.image, (j*const.tileSize, i*const.tileSize))
                if oneTile.hasAdvert():
                    self.background.blit(oneTile.advert.image, (j*const.tileSize+8, i*const.tileSize+1))
        
    
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
                        self.layout[i].append(tile.Tile(18, self.lang))
                    else:
                        self.layout[i].append(tile.Tile(8, self.lang))
                elif c == 1: # Floor
                    if lift: # Lift has special floor
                        self.layout[i].append(tile.Tile(4, self.lang))
                    else:
                        self.layout[i].append(tile.Tile(random.randint(1,3), self.lang))
                elif c == 2: # Shelf
                    self.layout[i].append(tile.Tile(random.randint(9,17), self.lang, self.roomDistance))
                elif c == 3: # Exit
                    self.exit = tile.Tile(0, self.lang)
                    self.layout[i].append(self.exit)
                elif c == 4: # Crate
                    self.layout[i].append(tile.Tile(5, self.lang))
                elif c == 5:
                    self.layout[i].append(tile.Tile(random.randint(1,3), self.lang))
                    halfLength = round((len(layout)-1)/2)
                    cartPos = (const.worldWidth/2+(j-halfLength)*const.tileSize, const.worldHeight/2+(i-halfLength)*const.tileSize)
                    self.carts.append(cart.Cart(cartPos, self.lang, self.roomDistance))
                elif c >= 60 and c <= 63:
                    self.layout[i].append(tile.Tile(random.randint(1,3), self.lang))
                    halfLength = round((len(layout)-1)/2)
                    npcPos = (const.worldWidth/2+(j-halfLength)*const.tileSize, const.worldHeight/2+(i-halfLength)*const.tileSize+3)
                    self.npcs.append(npc.Npc(npcPos,c-60))
                elif c == 7: # Water
                    self.layout[i].append(tile.Tile(19, self.lang))
                elif c >= 80 and c <= 83:
                    newTile = tile.Tile(7, self.lang)
                    newTile.setAdvert(c-80)
                    self.layout[i].append(newTile)
                elif c > 0:
                    self.layout[i].append(tile.Tile(4, self.lang))
                else:
                    raise ValueError(f'The room layout contains unknown value: {c}')
        # Set the neighbours for the tiles
        for i, row in enumerate(self.layout):
            for j, c in enumerate(row):
                if j: # Set the tile on top as neighbour if this isn't the top tile
                    self.layout[j-1][i].setNeighbour(0,c)
                if i: # Set the previous tile as neighbour if this isn't the first tile
                    self.layout[j][i-1].setNeighbour(1,c)
        # pair npcs with carts
        random.shuffle(self.carts)              # Shuffle carts to randomize pairing with npcs
        for i in range(min(len(self.npcs),len(self.carts))): # Zip the list with Nones as fillers
            if i < len(self.npcs):  npc1  = self.npcs[i]
            else:                   npc1  = None
            if i < len(self.carts): cart1 = self.carts[i]
            else:                   cart1 = None
            pair = (npc1, cart1)
            self.npcCartPairs.append(pair)
        #self.npcCartPairs = zip(self.npcs,self.carts)
