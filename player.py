import pygame, sys
from pygame.locals import *
import numpy as np
from utils import *
import os
import time
#from decal import Decal
from mysprite import *

class Player(BaseSprite):
    """ Watcha Gon' Do Playa' """
 
    def __init__(self, start_pos):
 
        image = pygame.image.load('images/player32.png')
        super(Player, self).__init__(start_pos, image)
 
        #self.dx = self.image.get_size()[0]
        #self.dy = self.image.get_size()[1]

        self.max_hit_pts = 3
        self.hit_pts = 2
        self.damage = 1    # ability to do damage
        equipmentl = EquipmentList()
        self.equipmentl = equipmentl
        self.level = 1
        self.powerups = None

        self.PM_MOVE = 0
        self.PM_BALLISTIC_SELECT = 1
        self.PM_BALLISTIC_FIRE = 2
        self.PM_TARGETING = 3
        self.mode = self.PM_MOVE

        self.ballistic = None
        self.equip_loc = None

        # sprite groups
        self.monsters = None
        self.all_sprites = None
        self.ballistic_sprites = None
        self.n_target_monster = None

        # This is REALLY dumb. monsters is a sprite group, which is NOT iterable.
        # So, we need something that is iterable, to select a monster when targeting.
        self.monster_list = None

        self.my_turn = True
        self.stun_rate = 2

        self.level_limits = [10000, 5200, 2000, 800]

    # Player changepos()
    def changepos(self, key):
        if self.key_is_equip(key):
            #self.use_equipment(key)
            if not self.key_is_equip(key): # Note this check is redundant if key_is_equip() is ALWAYS called first
                return
            self.equip_loc = key - pygame.K_1
            if VERBOSE:
                print( "Player.use_equipment(" +str(key) +"): equip_loc = " +str(self.equip_loc) )
                #print( "Player.use_equipment(): equipmentl = " +str(self.equipmentl) )
            if self.equipmentl.get(self.equip_loc):
                # If we got here, then the eqipment location is something other than none
                e = self.equipmentl.get(self.equip_loc)
                print( "Player.use_equipment(" +str(key) +"): equipmentl["+str(self.equip_loc) +"] = " +str(e) )
                if E_DAGGER == e or E_FIRE_BOMB == e:
                    self.mode = self.PM_BALLISTIC_SELECT
                    self.weapon = e
                if E_FIRESTORM == e or E_FREEZE_STORM == e or E_LIGHTNING == e:
                    self.mode = self.PM_TARGETING
                    self.weapon = e
        elif self.PM_MOVE == self.mode:
            self.change_x = 0
            self.change_y = 0
            if key == pygame.K_LEFT or (key == pygame.K_j):
                self.change_x = -self.dx
                self.my_turn = False
            elif key == pygame.K_RIGHT or key == pygame.K_l:
                self.change_x = self.dx
                self.my_turn = False
            elif key == pygame.K_UP or key == pygame.K_i:
                self.change_y = -self.dy
                self.my_turn = False
            elif key == pygame.K_DOWN or key == pygame.K_k:
                self.change_y = self.dy
                self.my_turn = False
            elif key == pygame.K_e:
                #print self.monsters
                #print len(self.monsters)
                if len(self.monsters) == 0:
                    # Note ladders is a sprite group, and can not be addressed as ldders[0]
                    for l in self.ladders: 
                        self.change_x = l.rect.x - self.rect.x
                        self.change_y = l.rect.y - self.rect.y
                    print ("exit to ladder:")
                    print ("   dx,dy  =:" +str(self.dx) +',' + str(self.dy))
                    print ("   ladder =:" +str(l.rect.x) +',' + str(l.rect.y))
                    print ("   change =:" +str(self.change_x) +',' + str(self.change_y))
                    #self.my_turn = False
        elif self.PM_BALLISTIC_SELECT == self.mode:
            if pygame.K_ESCAPE == key:
                self.mode = self.PM_MOVE
                self.weapon = None     #TODO: Do we need to define a mele weapon type??
                self.change_x = 0
                self.change_y = 0
                print "Returning to MOVE mode"

            elif self.key_is_move(key):
                ballistic_delta = 10
                ballistic_change_x = 0
                ballistic_change_y = 0
                if key == pygame.K_LEFT or (key == pygame.K_j):
                    ballistic_change_x = -ballistic_delta
                    print "my_ballistic LEFT"
                elif key == pygame.K_RIGHT or key == pygame.K_l:
                    ballistic_change_x = ballistic_delta
                    print "my_ballistic RIGHT"
                elif key == pygame.K_UP or key == pygame.K_i:
                    ballistic_change_y = -ballistic_delta
                    print "my_ballistic UP"
                elif key == pygame.K_DOWN or key == pygame.K_k:
                    ballistic_change_y = ballistic_delta
                    print "my_ballistic DOWN"

                self.my_ballistic = Ballistic((self.rect.x, self.rect.y), 
                        self.weapon, self.walls, self.monsters, 
                        ballistic_change_x, ballistic_change_y, self)
                self.ballistic_sprites.add(self.my_ballistic)
     
                # Decrement the equipmentl
                self.equipmentl.rm(self.equip_loc)
                self.equip_loc = None

                # Cleanup
                self.mode = self.PM_BALLISTIC_FIRE
                self.weapon = None     #TODO: Do we need to define a mele weapon type??
                print "Transitioning to FIRE mode"

        elif self.PM_BALLISTIC_FIRE == self.mode:
            #self.ballistic.update()
            pass

        elif self.PM_TARGETING == self.mode:
            #TODO: figure out keys (or mouse) for targeting: maybe 'n','p' for next,prev; and 'return' for commit?
            print "Player Target Mode"
            if pygame.K_ESCAPE == key:
                self.mode = self.PM_MOVE
                self.weapon = None     #TODO: Do we need to define a mele weapon type??
                self.n_target_monster = None
                self.equip_loc = None
                print "Returning to MOVE mode"

            if pygame.K_j == key or pygame.K_k == key or pygame.K_DOWN == key or pygame.K_UP == key :
                N = len(self.monster_list)
                if N == 0:
                    self.mode = self.PM_MOVE
                    self.weapon = None     #TODO: Do we need to define a mele weapon type??
                    self.n_target_monster = None
                    print "Returning to MOVE mode, targeting found no monsters"
                if pygame.K_k == key or pygame.K_DOWN == key:
                    if self.n_target_monster == None:
                        self.n_target_monster = 0
                    else:
                        if self.n_target_monster == N-1:
                            self.n_target_monster == 0
                        else:
                            self.n_target_monster += 1
                    print "Targeting (down) selected monster " +str(self.n_target_monster)
                if pygame.K_i == key or pygame.K_UP == key:
                    if self.n_target_monster == None:
                        self.n_target_monster = N-1
                    else:
                        if self.n_target_monster == N-1:
                            self.n_target_monster == N-1
                        else:
                            self.n_target_monster -= 1 
                    print "Targeting (up) selected monster " +str(self.n_target_monster)

            if pygame.K_RETURN == key:
                self.mode = self.PM_MOVE
                self.weapon = None     #TODO: Do we need to define a mele weapon type??
                self.n_target_monster = None
                print "Got a request to deploy a targeted weapon, but alas, targeting is not implemented"
                     
        else:
            print "Unknown Player Mode"
            sys.exit(0)


    def key_is_move(self, key):
        # TODO: Use w,a,s,d like arrow keys. Use h,j,k,l like vim
        if ( key == pygame.K_LEFT  or key == pygame.K_j or
             key == pygame.K_RIGHT or key == pygame.K_l or
             key == pygame.K_UP    or key == pygame.K_i or
             key == pygame.K_DOWN  or key == pygame.K_k ):
            return True
        else:
            return False

    def key_is_target_select(self, key):
        # TODO: Use w,a,s,d like arrow keys. Use h,j,k,l like vim
        if ( key == pygame.K_UP    or key == pygame.K_i or
             key == pygame.K_DOWN  or key == pygame.K_k ):
            return True
        else:
            return False

    def key_is_equip(self, key):
        if key >= pygame.K_1 and key <= pygame.K_9:
            equip_loc = key - pygame.K_1
            if equip_loc < self.equipmentl.length():
                return True
            else:
                return False
        else:
            return False

    def update(self):
        if self.PM_MOVE == self.mode:
            """ Update the player position. """
            # Move left/right
            self.rect.x += self.change_x
            self.rect.y += self.change_y
     
            # Did this update cause us to hit a wall?
            block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
            for block in block_hit_list:
                # Reset our position based on the left/right of the object.
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    self.rect.left = block.rect.right

                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom

                self.my_turn = True
                return
     
     
            # Check and see if we hit any Monsters
            block_hit_list = pygame.sprite.spritecollide(self, self.monsters, False)
            for block in block_hit_list:
                # If the monster is in 'Zombie' mode, then let us walk over him
                if block.resurection_cnt and block.hit_pts == 0:
                    pass

                else:
                    # Reset our position based on the left/right of the object.
                    if self.change_x > 0:
                        self.rect.right = block.rect.left
                    elif self.change_x < 0:
                        self.rect.left = block.rect.right

                    # Reset our position based on the top/bottom of the object.
                    if self.change_y > 0:
                        self.rect.bottom = block.rect.top
                    elif self.change_y < 0:
                        self.rect.top = block.rect.bottom

                    # Do the damage
                    #print "Player.update() Hit Monster: pre hit_pts = " +str(block.hit_pts)
                    #block.hit_pts -= self.damage
                    block.wound( self.damage, self.stun_rate )
                    #block.stun_level += self.stun_rate
                    print "Player.update() Hit Monster: new hit_pts = " +str(block.hit_pts)
                    if block.hit_pts <= 0:
                        if block.not_dead_yet or block.resurection_pts == 0:
                            self.add_exp_pts(block.exp_pts)
                            print "Dead Monster worth " +str(block.exp_pts) +" points"
                            block.not_dead_yet = False
                            #print str(type(block))
                            #block.prn()
                            print "Player killed Monster. now at " +str(self.exp_pts) +" exp points"
                            #self.prn()
                            if block.resurection_pts == 0:
                                self.monsters.remove(block)
                                block.kill()

            # Check and see if we hit the ladder
            block_hit_list = pygame.sprite.spritecollide(self, self.ladders, False)
            for block in block_hit_list:
                # Complete the level
                self.kill()

            self.change_x = 0
            self.change_y = 0
            
            if self.powerups: #TODO require powerups as part of __init__(), so we don't need this test?
                block_hit_list = pygame.sprite.spritecollide(self, self.powerups, True)
                for block in block_hit_list:
                    #if VERBOSE:
                    #    print "adding " +str(block.exp_pts) +" exp pts from powerup " +str(type(block)) +" = etype = " +str(block.e_type)
                    self.exp_pts += block.exp_pts
                    self.equipmentl.add( block.equip.e_type )
                    print self.equipmentl.get_list()

        elif self.PM_BALLISTIC_SELECT == self.mode:
            pass

        elif self.PM_BALLISTIC_FIRE == self.mode:
            if not self.my_ballistic.alive():
                self.add_exp_pts(self.my_ballistic.exp_pts)
                print "Dead Monster worth " +str(self.my_ballistic.exp_pts) +" points"
                print "Player killed Monster with my_ballistic. now at " +str(self.exp_pts) +" points"
                self.my_ballistic = None
                self.mode = self.PM_MOVE
                self.weapon = None     #TODO: Do we need to define a mele weapon type??
                print "Player.update(): my_ballistic hit something. Returning to MOVE mode"
                self.my_turn = False

        elif self.PM_TARGETING == self.mode:
            pass
        #print "Player.update complete"

    def add_exp_pts(self, pts):
        self.exp_pts += pts
        N = len( self.level_limits )
        for n in range(N):
            if self.exp_pts > self.level_limits[n]:
                if VERBOSE:
                    print "add_exp_pts: exp_pts = " +str(self.exp_pts) +" > level_limits[" +str(n) +"] = " +str(self.level_limits[n])
                self.level = (N-n) +1
                break
