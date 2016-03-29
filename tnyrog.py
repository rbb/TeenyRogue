import sys
import pygame
from pygame.locals import *
import numpy as np
import GameMap
from mysprite import *
from utils import *


N_MONSTERS = 1
N_POWERUPS = 2

gm = GameMap.game_map(MAP_W, MAP_H)
#gm.newrand()
#gm.newrandblocks()
gm.newrandsnake()
gm.clearpath()


# Setup the Window
pygame.init()
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
#font = pygame.font.SysFont("monospace", 15)
#font = pygame.font.SysFont("Arial", 15) 
screen = pygame.display.set_mode([SCREEN_W, SCREEN_H +STATUS_H])
pygame.display.set_caption('TnyRogue')


# Create the sprite group lists
all_sprite_list = pygame.sprite.Group()
powerup_list = pygame.sprite.Group()
monster_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
floor_list = pygame.sprite.Group()

#------------------------------------
# Make the walls. 
for x in range(MAP_W):
    for y in range(MAP_H):
        if gm.testwall(x, y):
            if gm.testwall(x,y+1):
                wall = Wall(x, y, SCALE, 'images/wall_gray.png')
            else:
                wall = Wall(x, y, SCALE, 'images/wall_gray_bot.png')
            wall_list.add(wall)
            all_sprite_list.add(wall)
        else:
            wall = Wall(x, y, SCALE, 'images/floor_gray.png')
            floor_list.add(wall)
            #all_sprite_list.add(wall)
if VERBOSE:
    print "Info: Walls Done"
    print "gm.m:"
    print gm.m

#------------------------------------
# Create the Ladder
ladder = Ladder( gm.ladder )
all_sprite_list.add(ladder)






#------------------------------------
# Create the Powerups
for n in range( N_POWERUPS ):
    p = Powerup( gm.randempty() )
    block_hit_list = True
    while block_hit_list:
        p = Powerup( gm.randempty() )
        block_hit_list = pygame.sprite.spritecollide(p, monster_list, False)
        if VERBOSE:
            print("Info: Redo powerup " +str(n))
    powerup_list.add(p)
    all_sprite_list.add(p)
if VERBOSE:
    print "Info: Powerups Done."
    print "powerups located at:"
    for p in powerup_list:
        print p.get_map_pos()
    print "- - - - - - - - - - - - - "





#------------------------------------
# Create the Monsters
for n in range( N_MONSTERS ):
    block_hit_monster_list = True
    block_hit_powerup_list = True
    while block_hit_monster_list or block_hit_powerup_list:
        m = Monster( gm.randempty() )
        block_hit_monster_list = pygame.sprite.spritecollide(m, monster_list, False)
        block_hit_powerup_list = pygame.sprite.spritecollide(m, powerup_list, False)
        #block_hit_powerup_list = []
        #if VERBOSE:
        #    print "m located at: " +str( m.get_map_pos() )
        #    print "block_hit_monster_list:"
        #    print block_hit_monster_list
        #    print "block_hit_powerup_list:"
        #    print block_hit_powerup_list
        #    print "------------------------------"

    m.walls = wall_list
    monster_list.add(m)
    all_sprite_list.add(m)
if VERBOSE:
    print "Info: Monsters Done."
 



#------------------------------------
# Create the player 
player = Player( gm.randempty() )
block_hit_monster_list = True
block_hit_powerup_list = True
while block_hit_monster_list or block_hit_powerup_list: 
    player = Player( gm.randempty() )
    block_hit_monster_list = pygame.sprite.spritecollide(player, monster_list, False)
    block_hit_powerup_list = pygame.sprite.spritecollide(player, powerup_list, False)
    if VERBOSE:
        print "Info: Redo player"
player.walls = wall_list
player.monsters = monster_list
player.powerups = powerup_list
all_sprite_list.add(player)
player.all_sprites = all_sprite_list

if VERBOSE:
    print "Info: Player Done."

 
#------------------------------------
# Make the Status bar
status = Status(0, SCREEN_H, SCREEN_W, STATUS_H, player)
all_sprite_list.add(status)

#------------------------------------
# Make the Level indicator
#print ("LEVEL_Y = " +str(LEVEL_Y) )
#level = Level(10, LEVEL_Y)
#level.player = player
#all_sprite_list.add(level)

#player.level=2

clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYUP:
            player.changepos(event.key)
            if event.key == pygame.K_q:
                done = True

    #floor_list.update()
    all_sprite_list.update()
    screen.fill(BLACK)
    floor_list.draw(screen)
    all_sprite_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
 
pygame.quit()

