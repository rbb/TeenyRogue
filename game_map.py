import numpy as np

 
def __init__(self, x=10, y=10):
    """
    0 = space
    1 = wall
    2 = player
    3 = monster
    """
    self.X = x
    self.Y = y
    self.M = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]] )
    self.m = self.M

    self.SPACE = 0
    self.WALL = 1

def newrand(self):
    # Start with a random array for a map, and then convert any above 0.5 into walls
    self.m = np.rand(self.X, self.Y)
    self.m[(self.m>0.5).nonzero()] = self.WALL

    # Force the edges to be walls
    self.m[0:X, 0] = self.WALL
    self.m[0:X, Y] = self.WALL
    self.m[0, 0:Y] = self.WALL
    self.m[X, 0:Y] = self.WALL
        
