#import sys
#import math
#import pygame
#from pygame.locals import *
import numpy as np
#import GameMap

# This is a quick an dirty script to read the map_attempts.txt file, which has
# data on the number of times a GameMap object had to be created in order to
# get a valid map, and calculate some very basic statistcs on it.

#with open("map_attempts.txt", "a") as myfile:
#    myfile.write( str(n_map_attempts) +"\n" )

d = np.genfromtxt('map_attempts.txt', delimiter=',')
print("Map Generation attempts")
print("Mean:    " +str( np.mean(d) ))
print("Std Dev: " +str( np.std(d) ))


