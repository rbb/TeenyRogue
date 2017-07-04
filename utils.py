import numpy as np

# -- Global constants
VERBOSE = 1
PNG_BG = False
MONSTER_MOVE = True     # Debug - set False to disable monster movement
TEST_MAP = False

if TEST_MAP:
    MAP_W = 5
    MAP_H = 5
else:
    MAP_W = 10
    MAP_H = 10
SCALE = 32
SCREEN_W = SCALE*MAP_W
SCREEN_H = SCALE*MAP_H
STATUS_H = 64 # 48
LEVEL_Y = SCREEN_H + STATUS_H/2 +1
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
PURPLE_DARK = (64, 32, 64)
PURPLE = (100, 12, 100)
GRAY = (128, 128, 128)
GRAY_25 = (64, 64, 64)
GRAY_37 = (94, 94, 94)
GRAY_40 = (102, 102, 102)
GRAY_45 = (115, 115, 115)
GRAY_50 = (128, 128, 128)
GRAY_75 = (192, 192, 192)
GREENISH = (67, 232, 43)
YELLOW = (244, 241, 0)
 
# Monster database
#                                 hit          moves/ exp  stopped  ballistic
#           Image name            pts, Damage, turn,  pts,  walls,    Damage,  Resurection
M_DATA = [["images/bomba32.png",   2,    1,     1,   200,    False,    True ,     0 ],    
          ["images/ghost32.png",   2,    1,     1,   100,    True ,    False,     0 ],
          ["images/knight32.png",  2,    2,     1,   250,    False,    False,     0 ],
          ["images/rat32.png",     1,    1,     1,    50,    False,    False,     0 ],
          ["images/skull32.png",   2,    1,     1,   100,    False,    False,     2  ],
          ["images/troll32.png",   2,    1,     1,   100,    False,    False,     0 ],
          ["images/wolf32.png",    2,    1,     2,   100,    False,    False,     0 ] ]
#          ["images/treasure32.png",0,    0,     0,   500,    False,    False,     0 ] ]
M_SKULL = 4

M_IMAGE_FNAME = 0
M_HIT_PTS = 1
M_DAMAGE = 2
M_MOVES = 3             # Number of moves/attacks per turn
M_EXP_PTS = 4           # Number of experience points earned for killing the monster
M_WALL_STOP = 5         # True: Walls stop movement, False: monster goes through walls
M_BALLISTIC = 6         # Attacks do ballistic damage
M_RESURECTION = 7       # Monster comes back from the dead, in this number of moves, if 0 then never.

#PU_IMAGES = ["images/dagger32.png", "images/firebomb32.png", "images/firestorm32.png", 
#             "images/freeze32.png", "images/lightning32.png" ]

#           Image Name             Function Name
L_DATA = [["images/thor.png",          "bonus_lightning"],
          ["images/bluedrop.png",      "bonus_freeze_throw"],
          ["images/flame.png",         "bonus_flame_throw"],
          ["images/flamebomb.png",     "bonus_flame_bomb"],
          ["images/freezebomb.png",    "bonus_freezebomb"],
          ["images/dagger32.png",      "bonus_dagger_damage"],
          ["images/dagger_bundle.png", "bonus_dagger_bundle"],
          ];

 
def randint(maxval=1):
    n_float = np.random.uniform(0, maxval-1)
    n = int(round( n_float ))
    #n = round( np.random.uniform(0, maxval-1) )
    #if VERBOSE:
    #    print ("randint.maxval = " +str(maxval) )
    #    print ("randint.n_float = " +str(n_float) )
    #    print ("randint.n = " +str(n) )
    return n
