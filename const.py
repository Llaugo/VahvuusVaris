import pygame
pygame.init()
import layoutLoader
# Initial world dimensions
worldWidth = 1400
worldHeight = 700

# Scale used for image sizes
# DON'T CHANGE from 1, not implemented to everywhere
scale = 1

# Different font sizes
xxsGameFont = pygame.font.SysFont(None, 17)
xsGameFont = pygame.font.SysFont(None, 23)
sGameFont = pygame.font.SysFont(None, 30)
mGameFont = pygame.font.SysFont(None, 50)
lGameFont = pygame.font.SysFont(None, 80)

# Tile size (square of (tileSize x tileSize))
tileSize = 46

# Player's base speed
basePlayerSpeed = 2

# How much time (sec) there is in each level (300 = 5min)
floorTime = 300
# Floor size (floorSize x floorSize rooms)
floorSize = 9

itemProbability = 0.05 # Probability that a shelf tile has an item on it
darknessProbability = 0.1 # Probability that a room is dark

# All the items that can appear in the shopping list and in the shop
# The first list has the most common items and the last list has the least common items
shop = [["Kirsikkatomaatti", "Satsuma", "Valkosipuli", "Myskikurpitsa", "Mango"],
        ["Välipalakeksi", "Fusilli", "Kaurahiutale", "Kvinoa", "Linssisipsit"],
        ["Rasvaton maito", "Kreikkalainen jogurtti", "Pakaste katkaravut", "Manchego", "Halloumi"],
        ["Kasvisliemikuutio", "Rosmariini", "Oliiviöljy", "Inkivääri", "Balsamico"],
        ["Viiriäisen munat", "Karambola", "Sahrami", "Murot", "Runebergin torttu"]]

# Item type rarities with cumulative distributions from the most common item type on the left to the rarest item type on the right.
# The item rarities change with respect to the room distance from the starting room
# Example: The first list tells that the starting room has 78% chance to spawn rarity 1 items
#          and 22% change to spawn rarity type 2 items. The rest of the items can't spawn there
itemRarity = [[0.78,	1,	1,	1,	1],
              [0.68,	0.95,	1,	1,	1],
              [0.59,	0.91,	0.99,	1,	1],
              [0.52,	0.85,	0.97,	0.99,	1],
              [0.45,	0.77,	0.95,	0.99,	1],
              [0.38,	0.66,	0.9,	0.97,	1],
              [0.32,	0.56,	0.81,	0.93,	1],
              [0.26,	0.47,	0.69,	0.86,	1],
              [0.2,	0.4,	0.6,	0.8,	1]]

'''
The rooms are created randomly from a list of predetermined layouts. 
One layout is a square of numbers, each number representing a type of tile.
0 = Wall
1 = Floor
2 = Shelf (Produces collectable items)
3 = Start
4 = Crate (can't be passed by without an active strength)
'''
lobbyLayout  = layoutLoader.readLayout("rooms/lift.csv")
startLayouts = layoutLoader.readLayout("rooms/startRooms.csv")
roomLayouts  = layoutLoader.readLayout("rooms/roomLayouts.csv")
testRoom     = layoutLoader.readLayout("rooms/testRoom.csv")