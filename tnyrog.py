import pygame, sys
from pygame.locals import *
import numpy as np
import GameMap
from mysprite import *


# -- Global constants
VERBOSE = 0
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
 
 
MAP_W= 10
MAP_H = 10
SCALE = 32
SCREEN_W= SCALE*MAP_W
SCREEN_H= SCALE*MAP_H

N_MONSTERS=2

gm = GameMap.game_map(MAP_W, MAP_H)
#gm.newrand()
#gm.newrandblocks()
gm.newrandsnake()
gm.clearpath()
 
 
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_W, SCREEN_H])
 
# Set the title of the window
pygame.display.set_caption('Test')
 
# List to hold all the sprites
all_sprite_list = pygame.sprite.Group()
powerup_list = pygame.sprite.Group()
monster_list = pygame.sprite.Group()
 
# Make the walls. (x_pos, y_pos, width, height)
wall_list = pygame.sprite.Group()
for x in range(MAP_W):
    for y in range(MAP_H):
        if gm.testwall(x,y):
            wall = Wall(x*SCALE,y*SCALE, SCALE, SCALE)
            wall_list.add(wall)
            all_sprite_list.add(wall)
 
#wall = Wall(10, 0, 790, 10)
#wall_list.add(wall)
#all_sprite_list.add(wall)

# Create the Powerups
for n in range( N_POWERUPS ):
    p = Powerup( gm.randempty() )
    block_hit_list = pygame.sprite.spritecollide(p, self.monster_list, False)
    while block_hist_list: 
        p = Monster( gm.randempty() )
        block_hit_list = pygame.sprite.spritecollide(p, self.monster_list, False)
        if VERBOSE:
            print ("Info: Redo powerup ", str(n))
    powerup_list.add(m)
    all_sprite_list.add(m)
 
# Create the Monsters
for n in range( N_MONSTERS ):
    m = Monster( gm.randempty() )
    block_hit_monster_list = pygame.sprite.spritecollide(m, self.monster_list, False)
    block_hit_powerup_list = pygame.sprite.spritecollide(m, self.powerup_list, False)
    while block_hist_list or block_hit_poweup_list: 
        m = Monster( gm.randempty() )
        block_hit_list = pygame.sprite.spritecollide(m, self.monster_list, False)
        block_hit_powerup_list = pygame.sprite.spritecollide(m, self.powerup_list, False)
        if VERBOSE:
            print ("Info: Redo monster ", str(n))
    powerup_list.add(m)
    all_sprite_list.add(m)
 
# Create the player object
player = Player( gm.randempty() )
block_hit_monster_list = pygame.sprite.spritecollide(player, self.monster_list, False)
block_hit_powerup_list = pygame.sprite.spritecollide(player, self.powerup_list, False)
while block_hist_list or block_hit_poweup_list: 
    player = Player( gm.randempty() )
    block_hit_list = pygame.sprite.spritecollide(player, self.monster_list, False)
    block_hit_powerup_list = pygame.sprite.spritecollide(player, self.powerup_list, False)
    if VERBOSE:
        print ("Info: Redo player")
player.walls = wall_list
all_sprite_list.add(player)

clock = pygame.time.Clock()
 
done = False
 
while not done:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #elif event.type == pygame.KEYDOWN:
        elif event.type == pygame.KEYUP:
            player.changepos(event.key)
            if event.key == pygame.K_q:
                done = True
 
    all_sprite_list.update()
    screen.fill(BLACK)
    all_sprite_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
 
pygame.quit()

