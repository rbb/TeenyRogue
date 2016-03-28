import numpy as np

# -- Global constants
VERBOSE = 1

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
GRAY_50 = (128, 128, 128)
GRAY_75 = (192, 192, 192)
GREENISH = (67, 232, 43)
 
# Monster database
#                                 hit          moves/ exp  stopped  ballistic
#           Image name            pts, Damage, turn,  pts,  walls,    Damage,  Resurection
M_DATA = [["images/bomba32.png",   2,    1,     1,    50,    False,    True ,     False ],    
          ["images/ghost32.png",   2,    1,     1,    50,    True ,    False,     False ],
          ["images/knight32.png",  2,    2,     1,    50,    False,    False,     False ],
          ["images/rat32.png",     1,    1,     1,    50,    False,    False,     False ],
          ["images/skull32.png",   2,    1,     1,    50,    False,    False,     True  ],
          ["images/troll32.png",   2,    1,     1,    50,    False,    False,     False ] ]
M_IMAGE_FNAME = 0
M_HIT_PTS = 1
M_DAMAGE = 2
M_MOVES = 3             # Number of moves/attacks per turn
M_EXP_PTS = 4           # Number of experience points earned for killing the monster
M_WALL_STOP = 5         # True: Walls stop movement, False: monster goes through walls
M_BALLISTIC = 6         # Attacks do ballistic damage

# Equipment database
#             Image Name          Damage, ballistic, global, targeting
E_DATA = [["images/dagger32.png",    1,      True,    False,  False ],
          ["images/firebomb32.png",  2,      True,    False,  False ],
          ["images/firestorm32.png", 1,      False,   True,   False ],
          ["images/freeze32.png",    1,      False,   True,   False ],
          ["images/lightning32.png", 1,      False,   False,  True  ] ]
E_DAGGER = 0
E_FIRE_BOMB = 1
E_FIRESTORM = 2
#E_FREEZE_BOMB = 3
E_FREEZE_STORM = 3
E_LIGHTNING = 4
# TODO other equipment


PU_IMAGES = ["images/dagger32.png", "images/firebomb32.png", "images/firestorm32.png", 
             "images/freeze32.png", "images/lightning32.png" ]

 
def randint(maxval=1):
    n_float = np.random.uniform(0, maxval-1)
    n = int(round( n_float ))
    #n = round( np.random.uniform(0, maxval-1) )
    #if VERBOSE:
    #    print ("randint.maxval = " +str(maxval) )
    #    print ("randint.n_float = " +str(n_float) )
    #    print ("randint.n = " +str(n) )
    return n
