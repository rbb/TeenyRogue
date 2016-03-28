import numpy as np
#import utils
from utils import *



SPACE = 0
WALL = 1
LADDER = 2

class game_map():
    def __init__(self, x=10, y=10):
        self.m = np.zeros([x, y])
        self.X = self.m.shape[0]
        self.Y = self.m.shape[1]
        self.setedges(WALL)              # edgewalls not defined yet!!

    #def randint(self, maxval=10):
    #    n = int(round(maxval * np.random.rand(1)[0]))
    #    return n

    def setblock(self, x1, y1, x2, y2, t):
        for x in range(x1, x2):
            for y in range(y1, y2):
                self.m[x,y] = t;

    def setedges(self, v):    # TODO: rename to finalize() or something?
        """Force the edges to be walls, and add a ladder"""
        #x = self.m.shape[0]
        #y = self.m.shape[1]
        x = self.X
        y = self.Y
        self.m[0:x, 0  ] = v
        self.m[0:x, y-1] = v
        self.m[0,   0:y] = v
        self.m[x-1, 0:y] = v

        self.ladder = self.randempty()
        self.m[self.ladder[0], self.ladder[1]] = LADDER



    #def edgewall(self):
    #    self.setedges(self, WALL)


    def newempty(self):
        self.m = np.zeros([self.X, self.Y])
        self.setedges(WALL)

    def newrand(self, limit=0.75):
        """Create a new random map"""
        self.m = np.random.rand(self.X, self.Y)
        self.m[(self.m>limit).nonzero()] = WALL
        self.m[(self.m<=limit).nonzero()] = SPACE
        self.setedges(WALL)

    def newrandblocks(self, N=10):
        """Create a new map with random blocks of walls"""
        for n in range(N):
            dx = randint(self.X/4)
            dy = randint(self.X/4)
            x1 = randint(self.X)
            y1 = randint(self.X)
            x2 = self.limitrange(x1 +dx, self.X)
            y2 = self.limitrange(y1 +dy, self.Y)
            self.setblock(x1, y1, x2, y2, WALL)
        self.setedges(WALL)

    def newrandsnake(self, N=8, M=5):
        """Create a new map with random blocks of walls"""
        for n in range(N):
            x = self.limitrange(randint(self.X), self.X)
            y = self.limitrange(randint(self.Y), self.Y)
            self.m[x,y] = WALL
            for m in range( randint(M) ):
                x = self.limitrange(x +randint(3) -1, self.X-1)
                y = self.limitrange(y +randint(3) -1, self.Y-1)
                self.m[x,y] = WALL
        self.setedges(WALL)
        

    def clearpath(self):
        """Check the map for mostly clear paths"""
        for x in range(1,self.X-1):
            for y in range(1,self.Y-1):
                if self.m[x,y] == WALL:
                    canpass= False
                    if x+1 < self.X -1:
                        if self.m[x+1, y] != WALL:
                            canpass = True
                    if x-1 > 1:
                        if self.m[x-1, y] != WALL:
                            canpass = True
                    if y+1 < self.Y-1:
                        if self.m[x, y+1] != WALL:
                            canpass = True
                    if y-1 > 1:
                        if self.m[x, y-1] != WALL:
                            canpass = True
                    if not canpass:
                        self.m[x,y] = SPACE

    def testwall(self, x, y):
        if x > self.X-1 or y > self.Y-1:
            return True
        if self.m[x,y] == WALL:
            return True
        return False

    def limitrange(self, a, A):
        if a > A -1:
            #print("++++++++++++++++++");
            a = A -1
        elif a < 0:
            #print("------------------");
            a = 0
        return a

    def randempty(self):
        tile = WALL
        while tile != SPACE:
            #if VERBOSE:
            #    print("game_map.X = " +str(self.X))
            x = randint(self.X)
            x = self.limitrange(x, self.X)
            y = randint(self.Y)
            y = self.limitrange(y, self.Y)
            tile = int(self.m[x, y])
            #if VERBOSE:
            #    print ("game_map.randempty: " +str([x, y, tile, SPACE]) )
        return x,y

