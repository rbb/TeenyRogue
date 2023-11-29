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
SCREEN_W = SCALE * MAP_W
SCREEN_H = SCALE * MAP_H
STATUS_H = 64  # 48
LEVEL_Y = SCREEN_H + STATUS_H / 2 + 1

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

# PU_IMAGES = ["images/dagger32.png", "images/firebomb32.png", "images/firestorm32.png",
#             "images/freeze32.png", "images/lightning32.png" ]

#           Image Name             Function Name
L_DATA = [["images/thor.png",          "bonus_lightning"],        # noqa: E241
          ["images/bluedrop.png",      "bonus_freeze_throw"],     # noqa: E241
          ["images/flame.png",         "bonus_flame_throw"],      # noqa: E241
          ["images/flamebomb.png",     "bonus_flame_bomb"],       # noqa: E241
          ["images/freezebomb.png",    "bonus_freezebomb"],       # noqa: E241
          ["images/dagger32.png",      "bonus_dagger_damage"],    # noqa: E241
          ["images/dagger_bundle.png", "bonus_dagger_bundle"],    # noqa: E241
          ]


def randint(maxval=1):
    n_float = np.random.uniform(0, maxval - 1)
    n = int(round(n_float))
    # n = round( np.random.uniform(0, maxval-1) )
    # if VERBOSE:
    #    print("randint.maxval = " +str(maxval) )
    #    print("randint.n_float = " +str(n_float) )
    #    print("randint.n = " +str(n) )
    return n
