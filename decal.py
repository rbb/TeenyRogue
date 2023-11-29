import pygame
# from pygame.locals import *
import utils

"""
-----
-***-
---*-
-***-
-*---
-***-
-----
"""


class Decal():    # pygame.sprite.Surface):
    """Base class for Monsters, Powerups, Player"""

    # Constructor function
    def __init__(self, color=utils.RED, size=1):
        # super(Decal, self).__init__()

        if size == 1:
            self.h = 14
            self.w = 10
            s = pygame.Surface((self.w, self.h))
            s.fill(utils.BLACK)

            zero = s.copy()
            pygame.draw.lines(zero, color, True, [(2, 2), (6, 2), (6, 10), (2, 10)], 1)

            one = s.copy()
            pygame.draw.lines(one, color, False, [(4, 2), (4, 10)], 1)

            two = s.copy()
            pygame.draw.lines(two, color, False, [(2, 2), (6, 2), (6, 6), (2, 6), (2, 10), (6, 10)], 1)

            three = s.copy()
            pygame.draw.lines(three, color, False, [(2, 2), (6, 2), (6, 6), (2, 6), (6, 6), (6, 10), (2, 10)], 1)

            four = s.copy()
            pygame.draw.lines(four, color, False, [(2, 2), (2, 6), (6, 6)], 1)
            pygame.draw.lines(four, color, False, [(6, 4), (6, 10)], 1)

            five = s.copy()
            pygame.draw.lines(five, color, False, [(6, 2), (2, 2), (2, 6), (6, 6), (6, 10), (2, 10)], 1)

            six = s.copy()
            pygame.draw.lines(six, color, False, [(2, 2), (2, 10), (6, 10), (6, 6), (2, 6)], 1)

            seven = s.copy()
            pygame.draw.lines(seven, color, False, [(2, 2), (6, 2), (6, 10)], 1)

        else:
            self.h = 7
            self.w = 5
            s = pygame.Surface((self.w, self.h))
            s.fill(utils.BLACK)

            zero = s.copy()
            pygame.draw.lines(zero, color, True, [(1, 1), (3, 1), (3, 5), (1, 5)], 1)

            one = s.copy()
            pygame.draw.lines(one, color, False, [(2, 1), (2, 5)], 1)

            two = s.copy()
            pygame.draw.lines(two, color, False, [(1, 1), (3, 1), (3, 3), (1, 3), (1, 5), (3, 5)], 1)

            three = s.copy()
            pygame.draw.lines(three, color, False, [(1, 1), (3, 1), (3, 3), (1, 3), (3, 3), (3, 5), (1, 5)], 1)

            four = s.copy()
            pygame.draw.lines(four, color, False, [(1, 1), (1, 3), (3, 3)], 1)
            pygame.draw.lines(four, color, False, [(3, 2), (3, 5)], 1)

            five = s.copy()
            pygame.draw.lines(five, color, False, [(3, 1), (1, 1), (1, 3), (3, 3), (3, 5), (1, 5)], 1)

            six = s.copy()
            pygame.draw.lines(six, color, False, [(1, 1), (1, 5), (3, 5), (3, 3), (1, 3)], 1)

            seven = s.copy()
            pygame.draw.lines(seven, color, False, [(1, 1), (3, 1), (3, 5)], 1)

        self.decals = [zero, one, two, three, four, five, six, seven]
        self.val = 0
        self.image = self.decals[self.val]
        self.setv(1)

    def setv(self, v):
        if v >= len(self.decals):
            return None
        self.val = v
        self.image = self.decals[self.val]
        return self.image

    def getv(self, v):
        return self.val + 1
