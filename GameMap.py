import numpy as np
#import utils
from utils import *



SPACE = 0
WALL = 1
LADDER = 2

VALID = 1
UNEXPLORED = 0    # For Valid matrix

class game_map():
    def __init__(self, x=10, y=3, ladder=None):
        # Note: numpy matrices are row(y) first, then column(x) !!!
        self.m = np.zeros([y, x], int)      # The map, not using 'map' because it is a keyword in python
        self.valid = np.zeros([y, x], int)      # The valid matrix, not using 'valid' because of the valid() function
        self.X = self.m.shape[1]
        self.Y = self.m.shape[0]
        self.ladder = None
        self.setedges(WALL, ladder)              # edgewalls not defined yet!!

    def setedges(self, v, ladder=None):    # TODO: rename to finalize() or something?
        """Force the edges to be walls, and add a ladder"""
        x = self.X
        y = self.Y
        self.m[0:y, 0  ] = v
        self.m[0:y, x-1] = v
        self.m[0,   0:x] = v
        self.m[y-1, 0:x] = v

        if ladder:
            self.ladder = ladder
        else:
            self.ladder = self.randempty()
        self.m[self.ladder[1], self.ladder[0]] = LADDER

    def newempty(self):
        self.m = np.zeros([self.Y, self.X])
        self.setedges(WALL)

    def newrand(self, limit=0.75):
        """Create a new random map"""
        self.ladder = None
        self.m = np.random.rand(self.Y, self.X)
        self.m[(self.m>limit).nonzero()] = WALL
        self.m[(self.m<=limit).nonzero()] = SPACE
        self.setedges(WALL)

    def setblock(self, x1, y1, x2, y2, v):
        #print "setblock: x1,y1,x2,y2,v = " +str([x1, y1, x2, y2, v])
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                self.m[y,x] = v;

    def newrandblocks(self, N=10):
        """Create a new map with random blocks of walls"""
        self.ladder = None
        #print "X,Y = " +str([self.X,self.Y]) +"    shape = " +str(self.m.shape)
        self.m = np.zeros( self.m.shape )
        self.X = self.m.shape[1]
        self.Y = self.m.shape[0]
        #print "X,Y = " +str([self.X,self.Y]) +"    shape = " +str(self.m.shape)
        #self.prn_m()
        #print "----"
        for n in range(N):
            dx = randint(self.X/4)
            dy = randint(self.Y/4)
            x1 = randint(self.X)
            y1 = randint(self.Y)
            x2 = self.limitrange(x1 +dx, self.X)
            y2 = self.limitrange(y1 +dy, self.Y)
            self.setblock(x1, y1, x2, y2, WALL)
            #self.prn_m()
            #print "----"
        self.setedges(WALL)

    def newrandsnake(self, N=8, M=5):
        """Create a new map with random blocks of walls"""
        self.ladder = None
        self.m = np.zeros( self.m.shape )
        for n in range(N):
            x = self.limitrange(randint(self.X), self.X)
            y = self.limitrange(randint(self.Y), self.Y)
            self.m[y,x] = WALL
            for m in range( randint(M) ):
                x = self.limitrange(x +randint(3) -1, self.X-1)
                y = self.limitrange(y +randint(3) -1, self.Y-1)
                self.m[y,x] = WALL
        self.setedges(WALL)
        

    def clearpath(self):
        """Check the map for mostly clear paths"""
        for x in range(1,self.X-1):
            for y in range(1,self.Y-1):
                if self.m[y,x] == WALL:
                    canpass= False
                    if x+1 < self.X -1:
                        if self.m[y, x+1] != WALL:
                            canpass = True
                    if x-1 > 1:
                        if self.m[y, x-1] != WALL:
                            canpass = True
                    if y+1 < self.Y-1:
                        if self.m[y+1, x] != WALL:
                            canpass = True
                    if y-1 > 1:
                        if self.m[y-1, x] != WALL:
                            canpass = True
                    if not canpass:
                        self.m[y,x] = SPACE

    def is_wall(self, x, y):
        if x > self.X-1 or y > self.Y-1:
            return True
        if self.m[y,x] == WALL:
            return True
        return False

    def is_ladder(self, x, y):
        if x > self.X-1 or y > self.Y-1:
            return False
        if self.m[y,x] == LADDER:
            return True
        return False

    def is_space(self, x, y):
        if x > self.X-1 or y > self.Y-1:
            return False
        if self.m[y,x] == SPACE:
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
            tile = int(self.m[y,x])
            #if VERBOSE:
            #    print ("game_map.randempty: " +str([x, y, tile, SPACE]) )
        return x,y

    def prn(self, matrix):
        """ Print a matrix in ASCII, to stdout"""
        s = ""
        for y in range(self.Y):
            for x in range(self.X):
                tile = matrix[y,x]
                if tile == WALL:
                    s += '##'
                elif tile == SPACE:
                    #s += '..'
                    s += "  "
                elif tile == LADDER:
                    s += '++'
                elif tile == UNEXPLORED:
                    s += 'vv'
            s += "\n"
        print s
    def prn_m(self):
        """ Print the map in ASCII, to stdout"""
        self.prn(self.m)
    def prn_valid(self):
        """ Print the valid results in ASCII, to stdout"""
        self.prn(self.valid)

    def next_space(self, x, y):
        """ Given the starting location x,y - find the next available space,
            searching accross, and then down. """
        tile = WALL
        while tile != SPACE:
            if x + 1< self.X:
                x += 1
            else:
                x = 1
                if y + 1< self.Y:
                    y += 1
                else:
                    return -1,-1
            #tile = int(self.m[y,x])
            tile = int(self.valid[y,x])
            return x,y

    def spread(self, sx, sy):
        if self.m[sy, sx] != WALL:
            self.valid[sy, sx] = 1;
        if self.m[sy-1, sx] != WALL and self.valid[sy-1, sx] == UNEXPLORED: # North
            self.spread(sx, sy-1)
        if self.m[sy, sx+1] != WALL and self.valid[sy, sx+1] == UNEXPLORED: # East
            self.spread(sx+1, sy)
        if self.m[sy+1, sx] != WALL and self.valid[sy+1, sx] == UNEXPLORED: # South
            self.spread(sx, sy+1)
        if self.m[sy, sx-1] != WALL and self.valid[sy, sx-1] == UNEXPLORED: # West
            self.spread(sx-1, sy)

    def is_valid(self):
        # set the valid matrix to UNEXPLORED
        self.valid = np.ones([self.Y, self.X], int) * UNEXPLORED

        # start by marking all the walls as valid
        for y in range(self.Y):
            for x in range(self.X):
                tile = self.m[y,x]
                if tile == WALL:
                    self.valid[y,x] = 1
        
        # Start looking at the spaces in the first upper left space.
        # Then find an adjacent space and mark it valid
        start_x = 0
        start_y = 1
        start_x, start_y = self.next_space(start_x, start_y)
        if start_x < 0:
            return False

        self.spread(start_x, start_y)

        #TODO: check if there is a valid path to the ladder from every square

        if np.all(self.valid):
            return True
        return False

        

