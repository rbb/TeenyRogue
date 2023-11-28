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

class MyGame():
    def __init__(self, TEST_MAP=False):
        self.TEST_MAP = TEST_MAP
        self.init_map()  # initializes self.gm
        print(self.gm)
        # Setup the Window
        pygame.init()

        # initialize font; must be called after 'pygame.init()' to avoid
        # 'Font not Initialized' error
        pygame.font.init()
        #font = pygame.font.SysFont("monospace", 15)
        self.FONT = pygame.font.SysFont("Arial", 15) 

        #pygame.display.init()
        self.screen = pygame.display.set_mode(
                [SCREEN_W, SCREEN_H +STATUS_H],
                #pygame.DOUBLEBUF|pygame.HWSURFACE,
                pygame.HWSURFACE,
                )
        pygame.display.set_caption('TnyRogue')

        print("")
        print(f"{self.screen.get_flags()=}")
        print("")
        self.level = 1
        self.done_game = False
        self.done_level = False
        self.player = None

        if TEST_MAP:
            self.N_MONSTERS = 1
            self.N_POWERUPS = 0
        else:
            self.N_MONSTERS = 1
            self.N_POWERUPS = 1
        print(self.gm)


    def init_map(self):
        if self.TEST_MAP:
            self.gm = GameMap.game_map(MAP_W, MAP_H)
            self.gm.m = np.array([ [ 1,1,1,1,1],
                              [ 1,0,1,0,1],
                              [ 1,0,1,0,1],
                              [ 1,0,0,0,1],
                              [ 1,1,1,1,1] ], int)
            self.gm.ladder = (3,1)

        else:
            print("init_map: MAP_W, MAP_H = " +str([MAP_W, MAP_H]))
            n_map_attempts = 0
            while True:
                self.gm = GameMap.game_map(MAP_W, MAP_H)
                #self.gm.newrand()
                #self.gm.newrandblocks()
                self.gm.newrandsnake()
                self.gm.clearpath()
                map_valid = self.gm.is_valid()
                print("map is_valid() = " +str(map_valid))
                n_map_attempts += 1
                print("Number of map attempts: " +str(n_map_attempts))
                if map_valid:
                    print("Saving number of map attempts: " +str(n_map_attempts) +" to file")
                    with open("map_attempts.txt", "a") as myfile:
                        myfile.write( str(n_map_attempts) +"\n" )
                    break


    #----------------------------------------------
    def do_level(self, player, Nmonsters, Npowerups):
    #----------------------------------------------
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
        for x in range(int(SCREEN_W/floor_rect.width)):
            for y in range(int(SCREEN_H/floor_rect.width)):
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
                if self.gm.is_wall(x, y):
                    if self.gm.is_wall(x,y+1):
                        #if PNG_BG:
                        wall = Wall(x, y, SCALE, wall_full)
                        #else:
                        #    wall = Wall(x, y, SCALE)
                    else:
                        wall = Wall(x, y, SCALE, wall_bot)
                    wall_group.add(wall)
                    all_sprite_group.add(wall)
                elif self.gm.is_space(x, y):
                    wall = Wall(x, y, SCALE, floor)
                    floor_group.add(wall)
                    #all_sprite_group.add(wall)
        if VERBOSE:
            print("Info: Walls and Floors Done")
            #print("self.gm.m:")
            #self.gm.prn_m()

        #------------------------------------
        # Create the Ladder
        ladder = Ladder( self.gm.ladder )
        ladder_group.add(ladder)
        all_sprite_group.add(ladder)


        #------------------------------------
        # Create the Powerups
        for n in range( self.N_POWERUPS ):
            p = Powerup( self.gm.randempty() )
            #block_hit_group = True
            #while block_hit_group:
            #    p = Powerup( gm.randempty() )
            #    block_hit_group = pygame.sprite.spritecollide(p, monster_group, False) #TODO: monster_group not populated yet
            #    if VERBOSE:
            #        print("Info: Redo powerup " +str(n))
            powerup_group.add(p)
            all_sprite_group.add(p)
        if VERBOSE:
            print("Info: Powerups Done.")
            print("powerups located at:")
            for p in powerup_group:
                print(p.get_map_pos())
            print("- - - - - - - - - - - - - ")


        #------------------------------------
        # Create the Monsters
        for n in range( Nmonsters ):
            block_hit_monster_group = True
            block_hit_powerup_group = True
            while block_hit_monster_group or block_hit_powerup_group:
                #if TEST_MAP:
                #    m = Monster( (3,2), self.gm )
                #else:
                #    m = Monster( self.gm.randempty(), self.gm )
                m = Monster( self.gm.randempty(), self.gm )
                #m = Monster( self.gm.randempty(), self.gm, M_SKULL )      #---------- DEBUG -------------
                #m = Monster( self.gm.randempty(), self.gm, 6 )      #---------- DEBUG -------------
                block_hit_monster_group = pygame.sprite.spritecollide(m, monster_group, False)
                block_hit_powerup_group = pygame.sprite.spritecollide(m, powerup_group, False)
                #block_hit_powerup_group = []
                #if VERBOSE:
                #    print("m located at: " +str( m.get_map_pos() ))
                #    print("block_hit_monster_group:")
                #    print(block_hit_monster_group)
                #    print("block_hit_powerup_group:")
                #    print(block_hit_powerup_group)
                #    print("------------------------------")

            m.walls = wall_group
            monster_group.add(m)
            monster_list.append(m)
            #all_sprite_group.add(m)
        if VERBOSE:
            print("Info: Monsters Done.")
         

        #------------------------------------
        # Create the player 
        block_hit_monster_group = True
        block_hit_powerup_group = True
        while block_hit_monster_group or block_hit_powerup_group: 
            if player == None:
                if TEST_MAP:
                    player = Player( (1,1) )
                else:
                    player = Player( self.gm.randempty() )
            else:
                if TEST_MAP:
                    player.set_map_pos( (1,1) )
                else:
                    player.set_map_pos( self.gm.randempty() )
            block_hit_monster_group = pygame.sprite.spritecollide(player, monster_group, False)
            block_hit_powerup_group = pygame.sprite.spritecollide(player, powerup_group, False)
            if VERBOSE:
                print("Info: Redo player")
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
            print("Info: Player Done.")

        #------------------------------------
        # Make the Status bar
        status = Status(0, SCREEN_H, SCREEN_W, STATUS_H, player, self.level,
                self.FONT)
        floor_group.add(status)
        all_sprite_group.add(status)

        #------------------------------------
        # Make the Level indicator
        #print("LEVEL_Y = " +str(LEVEL_Y) )
        #self.level = Level(10, LEVEL_Y)
        #self.level.player = player
        #all_sprite_group.add(self.level)

        #player.level=2

        clock = pygame.time.Clock()
        N = len(all_sprite_group)
        player.my_turn = True
        n_monster_turn = 0 
        monster_wait_n = 0     # Number of loops before processing next monster
        MONSTER_WAIT_N = 7     # Number of loops before processing next monster
        self.done_level = False
        
        while not self.done_level:
            if not player.my_turn and not monster_wait_n:
                if n_monster_turn >= len(monster_list):
                    n_monster_turn = 0
                    player.my_turn = True
                else:
                    # TODO: process monsters, starting with the one closest to the player, so that there is less chance of a backup/blockage
                    m = monster_list[n_monster_turn]
                    if m.hit_pts <= 0 and m.resurection_pts == 0:
                        del monster_list[n_monster_turn]
                    else:
                        print("acting on n_monster_turn = " +str(n_monster_turn ))
                        monster_list[n_monster_turn].my_turn = True
                        # TODO: separate Monster update() from changepos()/move() so that they can do ballistics
                        monster_list[n_monster_turn].changepos()
                        monster_list[n_monster_turn].my_turn = False
                    n_monster_turn += 1
                #print("n_monster_turn = " +str(n_monster_turn ) +"   len(monster_list) = " +str(len(monster_list)))
                monster_wait_n = MONSTER_WAIT_N

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.done_level = pygame.QUIT
                elif event.type == pygame.KEYUP and event.key == pygame.K_q:
                    self.done_level = pygame.QUIT
                elif event.type == pygame.KEYUP and event.key == pygame.K_p:
                    player.print_state()
                elif player.my_turn and event.type == pygame.KEYUP:
                    print("Player Turn")
                    player.changepos(event.key)   # TODO player.my_turn = False in changepos()
                    #player.update()

            # Update actions
            player.update()
            monster_group.update()
            ballistic_group.update()
            #all_sprite_group.update()

            # Do the rendering
            self.screen.fill(WHITE)
            self.screen.blit(bg, (0,0))
            status.update()
            floor_group.draw(self.screen)
            wall_group.draw(self.screen)
            powerup_group.draw(self.screen)
            ladder_group.draw(self.screen)
            monster_group.draw(self.screen)
            player_group.draw(self.screen)
            ballistic_group.draw(self.screen)
            #all_sprite_group.draw(self.screen)
            #pygame.display.flip()
            pygame.display.update()
            clock.tick(60)

            if player.hit_pts <= 0:
                self.done_level = pygame.QUIT
                self.done_game = True

            if not player.alive():
                # poor nomenclature: this means the sprite disapeared from
                # the screen
                print("Level " +str(self.level) +" Complete!")
                self.done_level = True  # TODO: move on to next level instead

            if monster_wait_n > 0 and not player.my_turn:
                monster_wait_n -= 1;

        player.heal(1)
        return player #End do_level()

    def level_monsters_powerups(self):
        #monsters = round(math.log10(self.level) +1.0)
        monsters = int(round(math.log10(self.level)*3.0 +1.0))
        powerups = randint(round(math.log10(self.level) +2.0))
        print("level, Nmonsters, Npowerups = " 
              +str( [self.level, monsters, powerups] )
              )
        return monsters, powerups

    def loop_levels(self):
        while not self.done_game:
            if self.TEST_MAP:
                Nmonsters = self.N_MONSTERS
                Npowerups = self.N_POWERUPS 
            else:
                Nmonsters, Npowerups = self.level_monsters_powerups()
            print(self.gm)
            self.player = self.do_level(self.player, Nmonsters, Npowerups)
            if self.done_level == True:
                self.player.exp_pts += 50
                self.level += 1
                self.init_map()

        print("")
        print("You DIED!!!!!!!!!!")
        print("Player Exp Pts: " +str(self.player.exp_pts))
        print("Player Level:   " +str(self.player.level))
        print("Dungeon Level:  " +str(self.level))
         
        self.done_game = False
        while not self.done_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.done_game = True
                elif event.type == pygame.KEYUP: # and event.key == pygame.K_q:
                    self.done_game = True
        pygame.quit()

def main():
    mg = MyGame()
    mg.loop_levels()

if __name__ == '__main__':
    main()
