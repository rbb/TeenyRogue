import pygame, sys
from pygame.locals import *
import numpy as np
from decal import *
from utils import *
import os

TD_SCREEN_W = SCALE*8
TD_SCREEN_H = SCALE*2

pygame.init()
screen = pygame.display.set_mode([TD_SCREEN_W, TD_SCREEN_H])
pygame.display.set_caption('Decal Test')

bg = pygame.Surface([TD_SCREEN_W, TD_SCREEN_H])
bg.fill(WHITE)

d_l = Decal(RED, 1)
d_s = Decal(RED, 0)
for v in range (8):
    d_l.setv(v)
    bg.blit(d_l.image, (v*32-d_l.w,32-d_l.h) )
    d_s.setv(v)
    bg.blit(d_s.image, (v*32-d_s.w,64-d_s.h) )


screen.fill(BLACK)
screen.blit(bg, (0,0))
pygame.display.update()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done = pygame.QUIT
        elif event.type == pygame.KEYUP and event.key == pygame.K_q:
            done = pygame.QUIT
