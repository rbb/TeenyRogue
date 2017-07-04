import sys
import math
import pygame
from pygame.locals import *
import numpy as np
import GameMap
from mysprite import *
from staticsprite import *
from player import *
from utils import *


if TEST_MAP:
    N_MONSTERS = 1
    N_POWERUPS = 0

    gm = GameMap.game_map(MAP_W, MAP_H)
    gm.m = np.array([ [ 1,1,1,1,1],
                      [ 1,0,1,0,1],
                      [ 1,0,1,0,1],
                      [ 1,0,0,0,1],
                      [ 1,1,1,1,1] ], int)
    gm.ladder = (3,1)

else:
    N_MONSTERS = 1
    N_POWERUPS = 1

    print "MAP_W, MAP_H = " +str([MAP_W, MAP_H])
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
pygame.font.init()
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
#font = pygame.font.SysFont("monospace", 15)
FONT = pygame.font.SysFont("Arial", 15) 
#pygame.display.init()
#screen = pygame.display.set_mode([SCREEN_W, SCREEN_H +STATUS_H], pygame.DOUBLEBUF|pygame.HWSURFACE)
screen = pygame.display.set_mode([SCREEN_W, SCREEN_H +STATUS_H], pygame.HWSURFACE)
pygame.display.set_caption('TnyRogue')

print ""
print "screen.get_flags() = " +str(screen.get_flags())
print ""

def do_level(level, player, gm, Nmonsters, Npowerups):
    bg = pygame.Surface([SCREEN_W, SCREEN_H +STATUS_H])
    bg.fill(BLACK)
    if PNG_BG:
        floor = pygame.image.load('images/floor_gray.png').convert()
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
    all_sprite_group = pygame.sprite.Group()
    ballistic_group = pygame.sprite.Group()
    powerup_group = pygame.sprite.Group()
    monster_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    floor_group = pygame.sprite.Group()
    ladder_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    monster_list = []

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
                wall_group.add(wall)
                all_sprite_group.add(wall)
            elif gm.is_space(x, y):
                wall = Wall(x, y, SCALE, floor)
                floor_group.add(wall)
                #all_sprite_group.add(wall)
    if VERBOSE:
        print "Info: Walls and Floors Done"
        #print "gm.m:"
        #gm.prn_m()

    #------------------------------------
    # Create the Ladder
    ladder = Ladder( gm.ladder )
    ladder_group.add(ladder)
    all_sprite_group.add(ladder)


    #------------------------------------
    # Create the Powerups
    for n in range( N_POWERUPS ):
        p = Powerup( gm.randempty() )
        #block_hit_group = True
        #while block_hit_group:
        #    p = Powerup( gm.randempty() )
        #    block_hit_group = pygame.sprite.spritecollide(p, monster_group, False) #TODO: monster_group not populated yet
        #    if VERBOSE:
        #        print("Info: Redo powerup " +str(n))
        powerup_group.add(p)
        all_sprite_group.add(p)
    if VERBOSE:
        print "Info: Powerups Done."
        print "powerups located at:"
        for p in powerup_group:
            print p.get_map_pos()
        print "- - - - - - - - - - - - - "


    #------------------------------------
    # Create the Monsters
    for n in range( Nmonsters ):
        block_hit_monster_group = True
        block_hit_powerup_group = True
        while block_hit_monster_group or block_hit_powerup_group:
            #if TEST_MAP:
            #    m = Monster( (3,2), gm )
            #else:
            #    m = Monster( gm.randempty(), gm )
            m = Monster( gm.randempty(), gm )
            #m = Monster( gm.randempty(), gm, M_SKULL )      #---------- DEBUG -------------
            #m = Monster( gm.randempty(), gm, 6 )      #---------- DEBUG -------------
            block_hit_monster_group = pygame.sprite.spritecollide(m, monster_group, False)
            block_hit_powerup_group = pygame.sprite.spritecollide(m, powerup_group, False)
            #block_hit_powerup_group = []
            #if VERBOSE:
            #    print "m located at: " +str( m.get_map_pos() )
            #    print "block_hit_monster_group:"
            #    print block_hit_monster_group
            #    print "block_hit_powerup_group:"
            #    print block_hit_powerup_group
            #    print "------------------------------"

        m.walls = wall_group
        monster_group.add(m)
        monster_list.append(m)
        #all_sprite_group.add(m)
    if VERBOSE:
        print "Info: Monsters Done."
     

    #------------------------------------
    # Create the player 
    block_hit_monster_group = True
    block_hit_powerup_group = True
    while block_hit_monster_group or block_hit_powerup_group: 
        if player == None:
            if TEST_MAP:
                player = Player( (1,1) )
            else:
                player = Player( gm.randempty() )
        else:
            if TEST_MAP:
                player.set_map_pos( (1,1) )
            else:
                player.set_map_pos( gm.randempty() )
        block_hit_monster_group = pygame.sprite.spritecollide(player, monster_group, False)
        block_hit_powerup_group = pygame.sprite.spritecollide(player, powerup_group, False)
        if VERBOSE:
            print "Info: Redo player"
    all_sprite_group.add(player)
    all_sprite_group.add(monster_group)
    player_group.add(player)

    turn_sprite_list = [player]
    for m in monster_group:
        turn_sprite_list.append(m)
        m.player = player
        m.players = player_group
        m.monsters = monster_group

    player.walls = wall_group
    player.monsters = monster_group
    player.monster_list = monster_list
    player.powerups = powerup_group
    player.ladders = ladder_group
    player.all_sprites = all_sprite_group
    player.ballistic_sprites  = ballistic_group


    if VERBOSE:
        print "Info: Player Done."

     
    #------------------------------------
    # Make the Status bar
    status = Status(0, SCREEN_H, SCREEN_W, STATUS_H, player, level, FONT)
    floor_group.add(status)
    all_sprite_group.add(status)

    #------------------------------------
    # Make the Level indicator
    #print ("LEVEL_Y = " +str(LEVEL_Y) )
    #level = Level(10, LEVEL_Y)
    #level.player = player
    #all_sprite_group.add(level)

    #player.level=2

    clock = pygame.time.Clock()
    done_level = False
    N = len(all_sprite_group)
    player.my_turn = True
    n_monster_turn = 0 
    while not done_level:
        if not player.my_turn:
            if n_monster_turn >= len(monster_list):
                n_monster_turn = 0
                player.my_turn = True
            else:
                m = monster_list[n_monster_turn]
                if m.hit_pts <= 0 and m.resurection_pts == 0:
                    del monster_list[n_monster_turn]
                else:
                    print "acting on n_monster_turn = " +str(n_monster_turn )
                    monster_list[n_monster_turn].my_turn = True
                    # TODO: separate Monster update() from changepos()/move() so that they can do ballistics
                    monster_list[n_monster_turn].changepos()
                    monster_list[n_monster_turn].my_turn = False
                n_monster_turn += 1
            print "n_monster_turn = " +str(n_monster_turn ) +"   len(monster_list) = " +str(len(monster_list))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                done_level = pygame.QUIT
            elif event.type == pygame.KEYUP and event.key == pygame.K_q:
                done_level = pygame.QUIT
            elif player.my_turn and event.type == pygame.KEYUP:
                print "Player Turn"
                player.changepos(event.key)   # TODO player.my_turn = False in changepos()
                #player.update()



        # Update actions
        player.update()
        monster_group.update()
        ballistic_group.update()
        #all_sprite_group.update()

        # Do the rendering
        screen.fill(WHITE)
        screen.blit(bg, (0,0))
        status.update()
        floor_group.draw(screen)
        wall_group.draw(screen)
        powerup_group.draw(screen)
        ladder_group.draw(screen)
        monster_group.draw(screen)
        player_group.draw(screen)
        ballistic_group.draw(screen)
        #all_sprite_group.draw(screen)
        #pygame.display.flip()
        pygame.display.update()
        clock.tick(60)

        if player.hit_pts <= 0:
            #done_level = True
            done_level = pygame.QUIT

        if not player.alive():   # poor nomenclature: this means the sprite disapeared from the screen
            print "Level " +str(level) +" Complete!"
            done_level = True  # TODO: move on to next level instead

    player.heal(1)
    return done_level, player #End do_level()

def level_monsters_powerups(level):
    #monsters = round(math.log10(level) +1.0)
    monsters = int(round(math.log10(level)*3.0 +1.0))
    powerups = randint(round(math.log10(level) +2.0))
    return monsters, powerups

level = 1
done_game = False
player = None

while not done_game:
    if TEST_MAP:
        Nmonsters = N_MONSTERS
        Npowerups = N_POWERUPS 
    else:
        Nmonsters, Npowerups = level_monsters_powerups(level)
    print "level, Nmonsters, Npowerups = " +str( [level, Nmonsters, Npowerups] )
    done_level, player = do_level(level, player, gm, Nmonsters, Npowerups)
    if player.hit_pts < 0:
        print "You DIED!!!!!!!!!!"
        done_game = True
    elif done_level == pygame.QUIT:
        done_game = True
    else:
        player.exp_pts += 50
        level += 1
        if not TEST_MAP:
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

print ""
print "Player Exp Pts: " +str(player.exp_pts)
print "Player Level:   " +str(player.level)
print "Dungeon Level:  " +str(level)
 
pygame.quit()

