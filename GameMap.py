import numpy as np
#import utils
from utils import *



SPACE = 0
WALL = 1
LADDER = 2

class game_map():
    def __init__(self, x=10, y=3):
        self.m = np.zeros([y, x])
        self.v = np.zeros([y, x])
        self.X = self.m.shape[1]
        self.Y = self.m.shape[0]
        self.setedges(WALL)              # edgewalls not defined yet!!
        #self.ladder = None

    def setblock(self, x1, y1, x2, y2, t):
        for x in range(x1, x2):
            for y in range(y1, y2):
                self.m[y,x] = t;

    def setedges(self, v):    # TODO: rename to finalize() or something?
        """Force the edges to be walls, and add a ladder"""
        #x = self.m.shape[0]
        #y = self.m.shape[1]
        x = self.X
        y = self.Y
        self.m[0:y, 0  ] = v
        self.m[0:y, x-1] = v
        self.m[0,   0:x] = v
        self.m[y-1, 0:x] = v

        #self.ladder = self.randempty()
        #self.m[self.ladder[0], self.ladder[1]] = LADDER

    def newempty(self):
        self.m = np.zeros([self.Y, self.X])
        self.setedges(WALL)

    def newrand(self, limit=0.75):
        """Create a new random map"""
        self.m = np.random.rand(self.Y, self.X)
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

    def testwall(self, x, y):
        if x > self.X-1 or y > self.Y-1:
            return True
        if self.m[y,x] == WALL:
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

    def prn(self):
        s = ""
        for y in range(self.m.shape[0]):
            for x in range(self.m.shape[1]):
                tile = self.m[y,x]
                if tile == WALL:
                    s += '##'
                elif tile == SPACE:
                    s += '  '
                elif tile == LADDER:
                    s += '++'
            s += "\n"
        #s += "\n"
        print s.strip()

    def next_space(self, x, y):
        """ Given the starting location x,y - find the next available space,
            searching accross, and then down. """
        tile = WALL
        while tile != SPACE:
            if x + 1< self.m.shape[1]:
                x += 1
            else:
                x = 1
                if y + 1< self.m.shape[0]:
                    y += 1
                else:
                    return -1,-1
            tile = int(self.m[y,x])
            return x,y

    def valid_path(self, sx, sy, ex, ey, heading=0, depth=0):
        """Verify that a particular path from a starting space to and end space can be reached."""
        """
        if VERBOSE:
            print "valid_path: " +str( [(sx, sy), (ex,ey)] )
        if sx == ex and sy == ey:
            return True
        elif ex > sx and sx+1 < self.m.shape[0] and self.m[sx+1, sy] != WALL:
            return self.valid_path(sx +1, sy, ex, ey)
        elif ey > sy and sy+1 < self.m.shape[1] and self.m[sy, sy+1] != WALL:
            return self.valid_path(sx, sy+1, ex, ey)
        elif ex < sx and sx-1 >= 0 and self.m[sx-1, sy] != WALL:
            return self.valid_path(sx-1, sy, ex, ey)
        elif ey < sy and sy-1 >= 0 and self.m[sx, sy-1] != WALL:
            return self.valid_path(sx, sy-1, ex, ey)
        else:
            return False
        """
        depth += 1
        if depth > 9:
            print "valid_path() Exiting because of deep recursion"
            return False

        up = 0
        right = 1
        down = 2
        left = 3
        

        if VERBOSE:
            print "valid_path: " +str( [(sx, sy), (ex,ey)] )
            print "            sx+1 =" +str(sx+1) +": " +str(self.m[sy, sx+1])
            print "            sx-1 =" +str(sx-1) +": " +str(self.m[sy, sx-1])
            print "            sy+1 =" +str(sy+1) +": " +str(self.m[sy+1, sx])
            print "            sy-1 =" +str(sy-1) +": " +str(self.m[sy-1, sx])

        ## Check exits clockwise
        #if sx == ex and sy == ey:
        #    return True
        #elif sx+1 < self.m.shape[1] and self.m[sy, sx+1] != WALL:
        #    return self.valid_path(sx+1, sy, ex, ey, depth)
        #elif sy+1 < self.m.shape[0] and self.m[sy+1, sx] != WALL:
        #    return self.valid_path(sx, sy+1, ex, ey, depth)
        #elif sx-1 >= 0              and self.m[sy, sx-1] != WALL:
        #    return self.valid_path(sx-1, sy, ex, ey, depth)
        #elif sy-1 >= 0              and self.m[sy-1, sx] != WALL:
        #    return self.valid_path(sx, sy-1, ex, ey, depth)
        #else:
        #    return False

        # east, south, west, north require that the entire map is surrounded by walls,
        # and that we are currently in a space to work.
        # TODO: perform error (bounds) checking when calculating north, east, south, west
        north = self.m[sy-1, sx]
        east  = self.m[sy, sx+1]
        south = self.m[sy+1, sx]
        west  = self.m[sy, sx-1]

        #if sx == ex and sy == ey:
        #    return True
        #elif east and west:
        #    # go east
        #else:
        #    return False

    def valid(self):
        """Verify that every (open) location can be reached."""
        
        # Start the search in the upper left
        start_x = 0
        start_y = 1

        start_x, start_y = self.next_space(start_x, start_y)
        if start_x < 0:
            return False

        for x in range(x1, x2):
            for y in range(y1, y2):
                if self.m[y,x] == WALL:
                    self.v[y,x] = 1;

        valid_spaces = []
        while start_x >= 0:
            x = start_x
            y = start_y
            while x >= 0:
                if (x,y) in valid_spaces:
                    x,y = next_space(x,y)
                else:
                    # search for a vaid path
                    pass
        
        






