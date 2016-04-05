import sys
import pygame
from pygame.locals import *
import numpy as np
import GameMap
from mysprite import *
from utils import *


N_MONSTERS = 1
N_POWERUPS = 2

while True:
    gm = GameMap.game_map(MAP_W, MAP_H)
    #gm.newrand()
    #gm.newrandblocks()
    gm.newrandsnake()
    gm.clearpath()
    valid = gm.is_valid()
    print "map is_valid() = " +str(valid)
    if valid:
        break


# Setup the Window
pygame.init()
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
#font = pygame.font.SysFont("monospace", 15)
#font = pygame.font.SysFont("Arial", 15) 
#pygame.display.init()
screen = pygame.display.set_mode([SCREEN_W, SCREEN_H +STATUS_H])
pygame.display.set_caption('TnyRogue')

bg = pygame.Surface([SCREEN_W, SCREEN_H +STATUS_H])
bg.fill(BLACK)
if PNG_BG:
    floor = pygame.image.load( 'images/floor_gray.png').convert()
else:
    floor = pygame.Surface([SCALE, SCALE])
    floor_rect = floor.get_rect()
    floor.fill(GRAY)
    pygame.draw.rect(floor, GRAY_45, (0,0, SCALE/2, SCALE/2), 1) 
    pygame.draw.rect(floor, GRAY_45, (SCALE/2+1,SCALE/2+1, SCALE/2-1, SCALE/2-1), 1) 
floor_rect = floor.get_rect()
for x in range(SCREEN_W/floor_rect.width):
    for y in range(SCREEN_H/floor_rect.width):
        floor_rect.topleft = (x * floor_rect.width, y * floor_rect.height)
        bg.blit(floor, floor_rect)

# Create the sprite group lists
all_sprite_list = pygame.sprite.Group()
powerup_list = pygame.sprite.Group()
monster_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
#floor_list = pygame.sprite.Group()
ladder_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()

#------------------------------------
# Make the walls. 
if PNG_BG:
    wall_full = pygame.image.load('images/wall_gray.png').convert()
    wall_bot = pygame.image.load('images/wall_gray_bot.png').convert()
else:
    wall_full = pygame.Surface([SCALE, SCALE])
    wall_full.fill(GRAY_37)

    wall_bot = pygame.Surface([SCALE, SCALE])
    wall_bot.fill(GRAY_37)
    pygame.draw.rect(wall_bot, GRAY_45, (SCALE*0/6,SCALE*5/6,   SCALE/6, SCALE/6), 1) 
    pygame.draw.rect(wall_bot, GRAY_45, (SCALE*1/6,SCALE*5/6-1, SCALE/6, SCALE/6+1), 1) 
    pygame.draw.rect(wall_bot, GRAY_45, (SCALE*2/6,SCALE*5/6,   SCALE/6, SCALE/6), 1) 
    pygame.draw.rect(wall_bot, GRAY_45, (SCALE*3/6,SCALE*5/6-1, SCALE/6, SCALE/6+1), 1) 
    pygame.draw.rect(wall_bot, GRAY_45, (SCALE*4/6,SCALE*5/6,   SCALE/6, SCALE/6), 1) 
    pygame.draw.rect(wall_bot, GRAY_45, (SCALE*5/6,SCALE*5/6-1, SCALE/6, SCALE/6+1), 1) 

for x in range(MAP_W):
    for y in range(MAP_H):
        if gm.is_wall(x, y):
            if gm.is_wall(x,y+1):
                #if PNG_BG:
                wall = Wall(x, y, SCALE, wall_full)
                #else:
                #    wall = Wall(x, y, SCALE)
            else:
                wall = Wall(x, y, SCALE, wall_bot)
            wall_list.add(wall)
            all_sprite_list.add(wall)
        #else:
        #    wall = Wall(x, y, SCALE, 'images/floor_gray.png')
        #    floor_list.add(wall)
        #    #all_sprite_list.add(wall)
if VERBOSE:
    print "Info: Walls Done"
    #print "gm.m:"
    #gm.prn_m()

#------------------------------------
# Create the Ladder
ladder = Ladder( gm.ladder )
ladder_list.add(ladder)
all_sprite_list.add(ladder)


#------------------------------------
# Create the Powerups
for n in range( N_POWERUPS ):
    p = Powerup( gm.randempty() )
    #block_hit_list = True
    #while block_hit_list:
    #    p = Powerup( gm.randempty() )
    #    block_hit_list = pygame.sprite.spritecollide(p, monster_list, False) #TODO: monster_list not populated yet
    #    if VERBOSE:
    #        print("Info: Redo powerup " +str(n))
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
        m = Monster( gm.randempty(), gm )
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
all_sprite_list.add(player)
player_list.add(player)

player.walls = wall_list
player.monsters = monster_list
player.powerups = powerup_list
player.ladders = ladder_list
player.all_sprites = all_sprite_list

for m in monster_list:
    m.player = player
    m.players = player_list
    this_monster_list = monster_list.copy()
    m.monsters = this_monster_list.remove(m)

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
    player.my_turn = True
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
    screen.blit(bg, (0,0))
    #floor_list.draw(screen)
    all_sprite_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

    if player.hit_pts < 0:
        print "You DIED!!!!!!!!!!"
        done = True

    if not player.alive():
        print "Level Complete!"
        done = True  # TODO: move on to next level instead
 
pygame.quit()

