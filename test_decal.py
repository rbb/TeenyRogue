import pygame
# from pygame.locals import *
import decal
import utils


TD_SCREEN_W = utils.SCALE * 8
TD_SCREEN_H = utils.SCALE * 2

pygame.init()
screen = pygame.display.set_mode([TD_SCREEN_W, TD_SCREEN_H])
pygame.display.set_caption('Decal Test')

bg = pygame.Surface([TD_SCREEN_W, TD_SCREEN_H])
bg.fill(utils.WHITE)

d_l = decal.Decal(utils.RED, 1)
d_s = decal.Decal(utils.RED, 0)
for v in range(8):
    d_l.setv(v)
    bg.blit(d_l.image, (v * 32 - d_l.w, 32 - d_l.h))
    d_s.setv(v)
    bg.blit(d_s.image, (v * 32 - d_s.w, 64 - d_s.h))


screen.fill(utils.BLACK)
screen.blit(bg, (0, 0))
pygame.display.update()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = pygame.QUIT
        elif event.type == pygame.KEYUP and event.key == pygame.K_q:
            done = pygame.QUIT
