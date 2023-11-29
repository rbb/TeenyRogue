import GameMap
import numpy as np

gm = GameMap.game_map(5, 10)
gm.prn_m()
print("\n")

print("------- edgewalls() ----------")
gm.setedges(0)
gm.prn_m()
gm.setedges(1)
gm.prn_m()
print("\n")


print("------- newrand() ----------")
gm.newrand()
gm.prn_m()
print(gm.m.mean())
print("\n")

print("------- clearpath() ----------")
gm.clearpath()
gm.prn_m()
print(gm.m.mean())
print("\n")


print("------- is_wall() ----------")
print(gm.is_wall(0, 0))
print(gm.is_wall(gm.X - 1, gm.Y - 1))
print(gm.is_wall(gm.X, gm.Y))
print("\n")


print("------- randempty() ----------")
print(gm.randempty())
print("\n")

print("------- newrandsnake() ----------")
gm.newrandsnake()
gm.prn_m()
ret_valid = gm.is_valid()
print("is_valid() returns: " + str(ret_valid))

N = 1000
snake_valids = np.zeros(N)
for n in range(N):
    gm.newrandsnake()
    snake_valids[n] = gm.is_valid()
print("average = " + str(snake_valids.mean()))
print("\n")

print("------- newrandblocks() ----------")
gm.newrandblocks()
gm.prn_m()
ret_valid = gm.is_valid()
print("is_valid() returns: " + str(ret_valid))

block_valids = np.zeros(N)
for n in range(N):
    gm.newrandblocks()
    block_valids[n] = gm.is_valid()
print("average = " + str(block_valids.mean()))
print("\n")

print("=========================================\n")
gm = GameMap.game_map(5, 5)
gm.m = np.array([[1, 1, 1, 1, 1],
                 [1, 0, 1, 0, 1],
                 [1, 1, 1, 1, 1],
                 [1, 0, 1, 0, 1],
                 [1, 1, 1, 1, 1], ])
gm.prn_m()
print(gm.m.mean())
print("------- clearpath() ----------")
gm.clearpath()
gm.prn_m()
print(gm.m.mean())
print("\n")
print("\n")

print("=========================================\n")
# gm = GameMap.game_map(5,6)
# gm.m = np.array([ [ 1,1,1,1,1],
#                  [ 1,0,1,0,1],
#                  [ 1,1,1,1,1],
#                  [ 1,0,1,0,1],
#                  [ 1,1,1,1,1],
#                  [ 1,1,1,1,1] ])
# gm.prn_m()
# print("shape = " +str(gm.m.shape))
# print("valid_path(1,1, 4,1) = " +str( gm.valid_path(1,1,4,1) ))
# #print("the non-valid map shows up as " +str(gm.valid()))
# print(("\n"))

gm = GameMap.game_map(5, 5)
gm.m = np.array([[1, 1, 1, 1, 1],
                 [1, 0, 1, 0, 1],
                 [1, 1, 1, 0, 1],
                 [1, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1], ])

# The expected output
valid = np.array([[1, 1, 1, 1, 1],
                  [1, 1, 1, 0, 1],
                  [1, 1, 1, 0, 1],
                  [1, 0, 0, 0, 1],
                  [1, 1, 1, 1, 1], ], int)
ret_valid = gm.is_valid()
print("is_valid() returns: " + str(ret_valid))
if np.all(ret_valid is False):
    print("is_valid() correct return")
else:
    print("is_valid() ERROR")


print("Expected gm.valid state")
gm.prn(valid)
print()
print("Test map output")
gm.prn_m()
print()
print("Actual gm.valid() state")
gm.prn_valid()

if np.all(gm.valid == valid):
    print("gm.valid state correct")
else:
    print("gm.valid state ERROR")

print("=========================================\n")
print("Checking diagnal path is only exit from a tile")

gm = GameMap.game_map(5, 5)
gm.m = np.array([[1, 1, 1, 1, 1],
                 [1, 1, 0, 1, 1],
                 [1, 0, 1, 1, 1],
                 [1, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1], ])

# The expected output
valid = np.array([[1, 1, 1, 1, 1],
                  [1, 1, 0, 1, 1],
                  [1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1], ], int)
ret_valid = gm.is_valid()
print("is_valid() returns: " + str(ret_valid))
if np.all(ret_valid is False):
    print("is_valid() correct return")
else:
    print("is_valid() ERROR")


print("Expected gm.valid state")
gm.prn(valid)
print()
print("Test map output")
gm.prn_m()
print()
print("Actual gm.valid() state")
gm.prn_valid()

if np.all(gm.valid == valid):
    print("gm.valid state correct")
else:
    print("gm.valid state ERROR")

print("=========================================\n")
N = 100
print("generating " + str(N) + " maps of size [10, 10] ...")
list_attempts = []
for n in range(N):
    n_map_attempts = 0
    while True:
        gm = GameMap.game_map(10, 10)
        # gm.newrand()
        # gm.newrandblocks()
        gm.newrandsnake()
        gm.clearpath()
        map_valid = gm.is_valid()
        # print "map is_valid() = " +str(map_valid)
        n_map_attempts += 1
        # print "iter: " +str(n) +"    attempts: " +str(n_map_attempts)
        if map_valid:
            break
    list_attempts.append(n_map_attempts)
np_attempts = np.array(list_attempts)
print("Map Generation attempts")
print("Mean:    " + str(np.mean(np_attempts)))
print("Std Dev: " + str(np.std(np_attempts)))
print("Max:     " + str(np.max(np_attempts)))
bins = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
h = np.histogram(np_attempts, bins)
print("Histogram bins " + str(bins))
print("Histogram      " + str(h[0]))
print("=========================================\n")
