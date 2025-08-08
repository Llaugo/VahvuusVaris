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
def gameFont(size=30):
    return pygame.font.SysFont("Courier", size)

# Tile size (square of (tileSize x tileSize))
tileSize = 46

# Player's base stats
basePlayerSpeed = 2
basePlayerStrength = 0
basePlayerSpeechDuration = 180

# How much time (sec) there is in each level (300 = 5min)
floorTime = 300
# Floor size (floorSize x floorSize rooms)
floorSize = 9

# NPC walking duration/distance
npcWalkDur = 93
npcWalkSpeed = 1

itemProbability = 0.05 # Probability that a shelf tile has an item on it
darknessProbability = 0.1 # Probability that a room is dark

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
# Maximum room distance from the start (and index for the "best" item distibution)
roomDistMax = len(itemRarity)-1

'''
The rooms are created randomly from a list of predetermined layouts. 
One layout is a square of numbers, each number representing a type of tile.
0 = Wall
1 = Floor
2 = Shelf (Produces collectable items)
3 = Start/Exit
4 = Crate (can't be passed by without an active strength)
5 = Cart
6 = NPC
7 = Water
8 = Advert screen
'''
lobbyLayout  = layoutLoader.readLayout("rooms/lift.csv")
startLayouts = layoutLoader.readLayout("rooms/startRooms.csv")
roomLayouts  = layoutLoader.readLayout("rooms/roomLayouts.csv")
testRoom     = layoutLoader.readLayout("rooms/testRoom.csv")

'''
All the words and sentences used in the game in different languages.
i=0: Suomi
i=1: English
i=2: Svenska
'''
phrase = [
["HISSIIN",                                 # 0: hissinapissa
     "Seuraava kerros",                     # 1: levelin aloitusnapissa
     "Kerros",                              # 2: checkpoint otsikon osa 1 & Kerrosnumeron edessä
     "suoritettu",                          # 3: checkpoint otsikon osa 2
     " OTA\nESINE",                         # 4: esinenapissa
     "TOINEN\nESINE",                       # 5: vaihda kaupattavaa esinettä
     "Huoneessa olevat esineet:",           # 6: huoneen esinelista
     "Ostoslista",                          # 7: Ostoslistan otsikko
     "AKTIVOI\nKORTTI",                     # 8: kortin aktivointinappi
     "Vahvistetaanko kauppa?",              # 9: kaupankäyntinäkymän otsikko
     "KYLLÄ",                               # 10: kaupankäynnin hyväksyntä
     "EI",                                  # 11: kaupankäynnin kielto
     "Takaisin päävalikkoon",               # 12: vahvuusvalikon paluunapissa
     "Arvo vahvuudet",                      # 13: vahvuuksien arpomisnapissa
     "Aloita seikkailu!",                   # 14: vahvuusvalikon hyväksymisnappi
     "Viisaus ja tieto",                    # 15: Vahvuusvalikon vahvuusotsikko
     "Rohkeus",                             # 16: ––––––––––––||––––––––––––
     "Inhimillisyys",                       # 17: ––––––––––––||––––––––––––
     "Oikeudenmukaisuus",                   # 18: ––––––––––––||––––––––––––
     "Kohtuullisuus",                       # 19: ––––––––––––||––––––––––––
     "Henkisyys",                           # 20: ––––––––––––||––––––––––––
     "Kirsikkatomaatti",                    # 21: Kaupan esineet ->
     "Satsuma",                             # 22
     "Valkosipuli",                         # 23
     "Myskikurpitsa",                       # 24
     "Mango",                               # 25
     "Välipalakeksi",                       # 26
     "Fusilli",                             # 27
     "Kaurahiutale",                        # 28
     "Kvinoa",                              # 29
     "Linssisipsit",                        # 30
     "Rasvaton maito",                      # 31
     "Kreikkalainen jogurtti",              # 32
     "Pakaste katkaravut",                  # 33
     "Manchego",                            # 34
     "Halloumi",                            # 35
     "Kasvisliemikuutio",                   # 36
     "Rosmariini",                          # 37
     "Oliiviöljy",                          # 38
     "Inkivääri",                           # 39
     "Balsamico",                           # 40
     "Viiriäisen munat",                    # 41
     "Karambola",                           # 42
     "Sahrami",                             # 43
     "Murot",                               # 44
     "Runebergin torttu",                   # 45 <- kaupan esineet
     "En näe laatikoita tutkittavaksi.",    # 46: uteliaisuuden aktivointi liian kaukana laatikoista
     "Huoneessa on jo valoisaa.",           # 47: oppimisen ilon aktivointi jos huoneessa ei ole pimeä
     "En näe tarjouksia lähettyvillä.",     # 48: rehellisyyden aktivointi ei käännä yhtään tarjousta & Sisu ei tuhoa yhtään tarjousta
     "En näe kärryjä huoneessa.",           # 49: Sosiaalisen älykkyyden aktivointi, jos kärryjä ei ole huoneessa
     "En näe kärryjen omistajia.",          # 50: Sosiaalisen älykkyyden aktivointi, jos ihmisiä ei ole huoneessa
     "En näe ketään ketä peilata.",         # 51: Myötätunnon aktivointi ilman ihmistä edessä
     "Ei ketään kenelle jutella.",          # 52: Reiluuden/Ryhmätyön/johtajuuden/rakkauden aktivointi ilman ihmistä edessä
     "Hänellä ei ole kärryjä.",             # 53: Reiluuden/johtajuuden aktivointi, kun ihmisellä ei ole kärryjä huoneessa
     "Ei ole esineitä millä käydä kauppaa.",# 54: Ryhmätyötaitojen aktivointi, kun ei ole esineitä kerättynä
     "En näe vettä kuivattavaksi.",         # 55: Anteeksiannon aktivointi ilman vettä lähellä
     "Kaikki hyllyt ovat jo täynnä jotakin kiinnostavaa.", # 56: kauneuden arvostuksen aktivointi, kun hyllyt ovat täynnä
     "Hänen kärrynsä ovat jumissa.",        # 57: johtajuuden aktivointi, kun NPC ei pääse kärrynsä luo
     "<3",                                  # 58: Rakkauden onnistunut aktivointi (lataa reppua)
     "",
     "",
     "",
     "Luovuuden lennokki",                  # ??: Vahvuuskorttien otsikot
     "Uteliaisuuden suurennuslasi",
     "Arviointikyvyn kaukoputki",
     "Oppimisen ilon hehkulamppu",
     "Näkökulmanottokyvyn nelikopteri",
     "Rohkeuden rukkaset",
     "Sinnikyyden saappaat",
     "Rehellisyyden radio",
     "Innostuksen juoksukengät",
     "Sisukkuuden sapeli",
     "Ystävällisyyden kukkakimppu",
     "Rakkauden rakettireppu",
     "Sosiaalisen älykkyyden silmälasit",
     "Myötätunnon peili",
     "Reiluuden lapaset",
     "Johtajuuden päähine",
     "Ryhmätyötaitojen tarjotin",
     "Anteeksiantavuuden pyyhe",
     "Vaatimattomuuden viitta",
     "Harkitsevuuden hörppy",
     "Itsesäätelyn suojakilpi",
     "Kauneuden arvostuksen kamera",
     "Kiitollisuuden kivet",
     "Toiveikkuuden taskulamppu",
     "Huumorintajun räpylät",
     "Hengellisyyden kynttilä",
     ""],
["EXIT",
     ""],
["HISSEN",
     ""]]

# All the items that can appear in the shopping list and in the shop
# The first list has the most common items and the last list has the least common items
def shop(lang):
    return [[phrase[lang][21], phrase[lang][22], phrase[lang][23], phrase[lang][24], phrase[lang][25]],
            [phrase[lang][26], phrase[lang][27], phrase[lang][28], phrase[lang][29], phrase[lang][30]],
            [phrase[lang][31], phrase[lang][32], phrase[lang][33], phrase[lang][34], phrase[lang][35]],
            [phrase[lang][36], phrase[lang][37], phrase[lang][38], phrase[lang][39], phrase[lang][40]],
            [phrase[lang][41], phrase[lang][42], phrase[lang][43], phrase[lang][44], phrase[lang][45]]]