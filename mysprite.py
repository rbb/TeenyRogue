import pygame, sys
from pygame.locals import *
import numpy as np
from utils import *
import os
import time
from decal import Decal

#TODO: Refactor E_* values and E_DATA into Equipment class
class Equipment:
    """A player's equipment list"""
    #def __init__(self, starting_equip=[E_DAGGER, E_NONE, E_NONE, E_NONE]):
    def __init__(self, starting_equip=[E_FIRESTORM, E_NONE, E_NONE, E_NONE]):
        self.e_list = starting_equip

    def add(self, e):
        """Add an equipment item (e) to the equipment list, in the next empty slot.

           Return False if no slots exist or if equipment type being added is invalid."""
        #Verify e is a valid eqipment type
        if not self.valid(e):
            return False

        for n in range( self.length() ):
            if self.e_list[n] == E_NONE:
                self.e_list[n] = e
                return True

        # If we get here, then we didn't find an empty slot
        return False

    def valid(self, e):
        if E_NONE == e or E_MAX <= e:
            return False
        else:
            return True

    def add_slots(self, dN=2):
        for n in range(dN):
            self.e_list.append( E_NONE )

    def get(self, n):
        return self.e_list[n]

    def rm(self, n):
        if E_NONE != self.e_list[n]:
            self.e_list[n] = E_NONE
            return True
        else:
            return False

    def get_list(self):
        return self.e_list

    def length(self):
        return len(self.e_list)


class BaseSprite(pygame.sprite.Sprite):
    """Base class for Monsters, Powerups, Player"""
 
    # Constructor function
    def __init__(self, start_pos, image):
        super(BaseSprite, self).__init__()
        self.image = image 
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.image.convert_alpha()
        self.set_map_pos(start_pos)
 
        # Set speed vector
        self.change_x = 0           # the commanded change this turn
        self.change_y = 0           # the commanded change this turn
        #self.dx = self.image.get_size()[0]
        #self.dy = self.image.get_size()[1]
        self.dx = SCALE             # This is the speed that the sprite will move normally
        self.dy = SCALE             # This is the speed that the sprite will move normally
        self.walls = None
        self.monsters = None
        self.ladders = None         # Note: using ladderS because it actually a sprite group, eventhough it only contains one sprite
        self.resurection_pts = 0    # This is how many turns a monster stays down before being re-animated, if 0 then the monster dies instead
        self.resurection_cnt = 0    # The current number of turns before being re-animated
        self.not_dead_yet = True

        self.my_ballistic = None
        self.ballistic_sprites = None
        self.hit_pts = 1
        self.damage = 1    # ability to do damage
        equipment = Equipment()
        self.equipment = equipment
        self.exp_pts = 0
 
    def set_map_pos(self, start_pos):
        self.rect.y = start_pos[1] * SCALE   # Note: rect is graphic position, not map position
        self.rect.x = start_pos[0] * SCALE   # Note: rect is graphic position, not map position

    def get_map_pos(self):
        return (self.rect.x / SCALE, self.rect.y / SCALE)

    def changepos(self, key):
        self.change_x = 0
        self.change_y = 0
        #if key == pygame.K_LEFT:
        #    self.change_x = -self.dx
        #elif key == pygame.K_RIGHT:
        #    self.change_x = self.dx
        #elif key == pygame.K_UP:
        #    self.change_y = -self.dy
        #elif key == pygame.K_DOWN:
        #    self.change_y = self.dy

    def update(self):      # BaseSprite
        pass
 
    def prn(self):
        """print some basic (debug) info about BaseSprites"""
        if VERBOSE:
            print "change_x,y:" +str([self.change_x, self.change_y])
            print "dx,y:      " +str([self.dx, self.dy])
            print "hit_pts:   " +str(self.hit_pts)
            print "exp_pts:   " +str(self.exp_pts)
            print "damage:    " +str(self.damage)
            #print "monsters:    " +str(self.monsters)
            #print "walls:    " +str(self.walls)

    def move_collision (self, sprite_group):
        """BaseSprite Collision Detection"""
        block_hit_list = pygame.sprite.spritecollide(self, sprite_group, False)
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

            return True
        return False

    def wound (self, pts, stun):
        if self.hit_pts > 0:
            self.hit_pts -= pts
        if self.hit_pts < 0:
            self.hit_pts = 0     # Note: this should be redunant now, but keep it as a recovery mechanism
        if self.resurection_pts > 0 and self.hit_pts == 0:
            self.resurection_cnt = self.resurection_pts
        else:
            self.stun_level += stun

    def heal(self, pts):
        self.hit_pts += pts
        if self.hit_pts > self.max_hit_pts:
            self.hit_pts = self.max_hit_pts
 

class Powerup(BaseSprite):
    """ Powerups that the player can grab"""

    def __init__(self, start_pos, e_type=None):
        # Call the parent's constructor
 
        #print (str(PU_IMAGES) )
        if (e_type == None):
            self.e_type = 0
            while self.e_type == 0:
                self.e_type = int(round( np.random.uniform(0, len(E_DATA)-1) ))
        else:
            self.e_type = e_type
        #fname = PU_IMAGES[ self.e_type ] 
        fname = E_DATA[self.e_type][E_IMAGE]
        if None == fname:
            print "Powerup.__init__(): Error - fname == None"
            print "Powerup.__init__(): e_type = " +str(e_type)
            print "Powerup.__init__(): self.e_type = " +str(self.e_type)
            #print "Powerup.__init__(): fname = " +str(fname)
            sys.exit(0)
        image = pygame.image.load( fname )
        super(Powerup, self).__init__(start_pos, image)
        self.exp_pts = E_DATA[self.e_type][E_EXP_PTS]

    def changepos(self, key):
        self.change_x = 0
        self.change_y = 0
        #if key == pygame.K_LEFT:
        #    self.change_x = -self.dx
        #elif key == pygame.K_RIGHT:
        #    self.change_x = self.dx
        #elif key == pygame.K_UP:
        #    self.change_y = -self.dy
        #elif key == pygame.K_DOWN:
        #    self.change_y = self.dy

    def update(self):      # Powerup
        pass
 

class Ballistic(BaseSprite):
    """Things that the player can shoot"""

    def __init__(self, start_graph_pos, e_type, walls, monsters, change_x, change_y, parent):
        if (e_type == None):
            self.e_type = int(round( np.random.uniform(0, len(E_DATA)-1) ))
        else:
            self.e_type = e_type
        fname = E_DATA[self.e_type][E_IMAGE]
        if None == fname:
            print "Ballistic.__init__(): Error - fname == None"
            sys.exit(0)
        image = pygame.image.load( fname )
        start_pos = [start_graph_pos[0] / SCALE, start_graph_pos[1] / SCALE]
        super(Ballistic, self).__init__(start_pos, image)
        #self.rect.y = start_pos[1]   # Note: rect is graphic position, not map position
        #self.rect.x = start_pos[0]   # Note: rect is graphic position, not map position
        self.damage = E_DATA[self.e_type][E_DAMAGE]
        self.walls = walls
        self.monsters = monsters
        self.change_x = change_x
        self.change_y = change_y
        self.exp_pts = 0      # Use Ballistic.exp_pts as a pass through for the monster killed
        self.parent = parent
        if VERBOSE:
            print "Ballistic.__init__(): e_type = " +str(e_type)
            print "Ballistic.__init__(): self.e_type = " +str(self.e_type)
            print "Ballistic.__init__(): fname = " +str(fname)
            print "Ballistic.__init__(): change_x = " +str(change_x)
            print "Ballistic.__init__(): change_y = " +str(change_y)

    def changepos(self, key):
        pass

    def update(self):   # Ballistic
        """ Update the Ballistic position. """
        super(Ballistic, self).update()
        #if VERBOSE:
        #    print "Ballistic.update(): x,y = " +str([self.rect.x, self.rect.y])
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.monsters, False)
        for block in block_hit_list:
            print "Ballistic.update() Hit Monster: pre hit_pts = " +str(block.hit_pts)
            block.hit_pts -= self.damage
            print "Ballistic.update() Hit Monster: new hit_pts = " +str(block.hit_pts)
            if block.hit_pts <= 0:
                print "Dead Monster. Do SOMETHING!!!!"
                self.exp_pts = block.exp_pts
                self.monsters.remove(block)
                block.kill()
                self.parent.update()
                #TODO: block = None, so that memory gets cleared??? Maybe we just wait until the next level of monsters is created???
            #TODO: Create a hit flash/explosion/something
            #self.mark_for_del()
            self.kill()

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            #self.mark_for_del()
            self.kill()
            print "Ballistic.update(): Hit a Wall!"


    def active(self):
        if self.image:
            return True
        else: 
            return False

class Stun:
    """Object to hold stun sprites"""
    def __init__(self, image):
        """
        self.STUN1 = pygame.Surface([SCALE, SCALE])
        self.STUN1.set_alpha(128)
        pygame.draw.line(self.STUN1, YELLOW, (13,11), (18,11), 1) 
        pygame.draw.line(self.STUN1, YELLOW, (13,0), (18,0), 1) 
        pygame.draw.line(self.STUN1, YELLOW, (7,4), (7,7), 1) 
        pygame.draw.line(self.STUN1, YELLOW, (24,4), (24,7), 1) 

        self.STUN2 = pygame.Surface([SCALE, SCALE])
        self.STUN2.set_alpha(128)
        pygame.draw.line(self.STUN2, YELLOW, (24,4), (21,1), 1) 
        pygame.draw.line(self.STUN2, YELLOW, (13,0), (10,1), 1) 
        pygame.draw.line(self.STUN2, YELLOW, (7,7), (10,10), 1) 
        pygame.draw.line(self.STUN2, YELLOW, (18,11), (21,10), 1) 

        self.STUN3 = pygame.Surface([SCALE, SCALE])
        self.STUN3.set_alpha(128)
        pygame.draw.line(self.STUN3, YELLOW, (21,10), (24,7), 1) 
        pygame.draw.line(self.STUN3, YELLOW, (21,1), (18,0), 1) 
        pygame.draw.line(self.STUN3, YELLOW, (10,1), (7,4), 1) 
        pygame.draw.line(self.STUN3, YELLOW, (18,10), (13,11), 1) 

        self.n = 0
        self.sprite_list = [self.STUN1, self.STUN2, self.STUN3]
        self.sprite = self.STUN1
        """
        self.lines = []
        self.lines.append( [ (13,11), (18,11), (13,0), (18,0), (7,4), (7,7), (24,4), (24,7) ]   )
        self.lines.append( [ (24,4), (21,1), (13,0), (10,1), (7,7), (10,10), (18,11), (21,10) ] )
        self.lines.append( [ (21,10), (24,7), (21,1), (18,0), (10,1), (7,4), (18,10), (13,11) ] )

        self.base_image = image.copy()
        self.sprite = image.copy()
        self.n = 0
        self.DIV = 8
        self.draw_stun()


    def draw_stun(self):
        m = self.n/self.DIV
        self.sprite = self.base_image.copy()
        pygame.draw.line(self.sprite, YELLOW, self.lines[m][0], self.lines[m][1], 1) 
        pygame.draw.line(self.sprite, YELLOW, self.lines[m][2], self.lines[m][3], 1) 
        pygame.draw.line(self.sprite, YELLOW, self.lines[m][4], self.lines[m][5], 1) 
        pygame.draw.line(self.sprite, YELLOW, self.lines[m][6], self.lines[m][7], 1) 

    def next(self):
        self.n += 1
        if self.n >= len(self.lines)*self.DIV:
            self.n = 0
        #self.sprite = self.sprite_list[self.n/self.DIV]
        self.draw_stun()

class Monster(BaseSprite):
    """ Monsters. Need I say more? """
 
    def __init__(self, start_pos, level_map, m_type=None):
        #image = pygame.image.load('images/knight32.png')
        #super(Monster, self).__init__(start_pos, image)
        #BaseSprite.__init__(self, start_pos, image)

        if (m_type == None):
            self.m_type = int(round( np.random.uniform(0, len(M_DATA)-1) ))
        else:
            self.m_type = m_type
        fname = M_DATA[self.m_type][M_IMAGE_FNAME] 
        image = pygame.image.load( fname )
        #image.scroll(0, -1)
        super(Monster, self).__init__(start_pos, image)
        self.base_image = image
        self.hit_pts = M_DATA[self.m_type][M_HIT_PTS] 
        self.max_hit_pts = M_DATA[self.m_type][M_HIT_PTS] 
        self.moves = M_DATA[self.m_type][M_MOVES] 
        self.wall_stop = M_DATA[self.m_type][M_WALL_STOP] 
        self.ballistic = M_DATA[self.m_type][M_BALLISTIC] 
        self.resurection_pts = M_DATA[self.m_type][M_RESURECTION] 
        self.exp_pts = M_DATA[self.m_type][M_EXP_PTS] 
        self.damage = M_DATA[self.m_type][M_DAMAGE] 
        self.player = None
        self.players = None
        self.monsters = None
        self.level_map = level_map
        self.stun_level = 0
        self.recover_rate = 1
        self.stun = Stun(self.image)
        self.hit_decal = Decal(RED, 1)
        self.hit_decal.setv(self.hit_pts)
        if VERBOSE:
            print ("Monster.fname = " +str(fname) )
            print ("Monster.hit_pts = " +str(self.hit_pts) )
            print ("Monster.exp_pts = " +str(self.exp_pts) )

    #def __getattr__(self, name):
    #    return getattr(self.BaseSprite, name)
    def changepos(self):
        """ Update the Monster position, etc """
        print "Monster.changepos: type = " +M_DATA[self.m_type][M_IMAGE_FNAME]
        if not MONSTER_MOVE:
            return
        if self.player.hit_pts <= 0:
            return
        if self.player.my_turn:
            if VERBOSE:
                print "WARNING: Monster.changepos() during player's turn"
            return

        if self.stun_level > 0:
            self.stun_level -= self.recover_rate
            if self.stun_level < 0:
                self.stun_level = 0
            if VERBOSE:
                print "Monster stunned. Recovered to stun_level = " +str(self.stun_level)
            return

        for n in range(self.moves,0,-1):
            self.find_move()
            if n > 1:
                if VERBOSE:
                    print "Monster.changepos: doing intermediate update()"
                self.update()
                pygame.time.wait( 200 ) #milliseconds

        
    def find_move(self):
        """ The logic for the moster movement (AI) """
        # First, check to see if we're dead, waiting to be resurected
        if self.hit_pts == 0:
            self.resurection_cnt -= 1
            print "Monster.find_move: resurection_cnt = " +str(self.resurection_cnt)
            if self.resurection_cnt <= 0:
                self.heal( self.resurection_pts )
            else:
                return

        # First, try to move towards the player
        collision = False
        x,y = self.get_map_pos()
        px,py = self.player.get_map_pos()
        dx = px - x
        dy = py - y
        d = abs(dy) - abs(dx) # d > 1 means y larger, d < 0 means x larger
        dsum = abs(dy) + abs(dx) # dsum = 1 means player directly adjacent
        if VERBOSE:
            print "Monster.find_move: x,y = " +str([x,y]) +",   px,py = " +str([px,py])
            print "Monster.find_move: dx,dy = " +str([dx,dy]) +",   d = " +str(d) +",   dsum = " +str(dsum)

        # attack directly if adjacent
        if dsum == 1:
            # If we attack directly adjacent, then we don't need to move the sprite
            #if dy == 1:
            #    self.move(0, SCALE)
            #elif dy == -1:
            #    self.move(0, -SCALE)
            #elif dx == 1:
            #    self.move(SCALE, 0)
            #elif dx == -1:
            #    self.move(-SCALE, 0)

            # Did this update cause us to hit the player
            #if move_collision (self, self.players):
            #block_hit_list = pygame.sprite.spritecollide(self, self.players, False)
            #for block in block_hit_list:
            #    # Do the damage
            #    self.player.hit_pts -= self.damage
            #    print "Monster.changepos() Hit Player: new hit_pts = " +str(self.player.hit_pts)
            #    if self.player.hit_pts < 0:
            #        return
            # Do the damage
            self.player.hit_pts -= self.damage
            if VERBOSE:
                print "Monster.find_move() Hit Player: new hit_pts = " +str(self.player.hit_pts)
            #if self.player.hit_pts < 0:
            #    return
            return

        # Not adjacent to player, so move towards them
        # Go the farther direction first
        if d >= 0 and dy > 0 and not self.level_map.is_wall(x, y +1):
            collision = self.move(0, SCALE)
            if not collision:
                if VERBOSE:
                    print "Monster.find_move() going South towards player"
                return
        if d >= 0 and dy < 0 and not self.level_map.is_wall(x, y -1):
            collision = self.move(0, -SCALE)
            if not collision:
                if VERBOSE:
                    print "Monster.find_move() going North towards player"
                return
        if d < 0 and dx > 0 and not self.level_map.is_wall(x +1, y):
            collision = self.move(SCALE, 0)
            if not collision:
                if VERBOSE:
                    print "Monster.find_move() going East towards player"
                return
        if d < 0 and dx < 0 and not self.level_map.is_wall(x -1, y):
            collision = self.move(-SCALE, 0)
            if not collision:
                if VERBOSE:
                    print "Monster.find_move() going West towards player"
                return

        # We can't head directly towards player
        # So, try to go perpendicular
        if d < 0 and dy > 0 and not self.level_map.is_wall(x, y +1):
            collision = self.move(0, SCALE)
            if not collision:
                if VERBOSE:
                    print "Monster.find_move() going South"
                return
        if d < 0 and dy < 0 and not self.level_map.is_wall(x, y -1):
            collision = self.move(0, -SCALE)
            if not collision:
                if VERBOSE:
                    print "Monster.find_move() going North"
                return
        if d >= 0 and dx > 0 and not self.level_map.is_wall(x +1, y):
            collision = self.move(SCALE, 0)
            if VERBOSE:
                if not collision:
                    print "Monster.find_move() going East"
                return
        if d >= 0 and dx < 0 and not self.level_map.is_wall(x -1, y):
            collision = self.move(-SCALE, 0)
            if not collision:
                if VERBOSE:
                    print "Monster.find_move() going West"
                return

        # If we can't figure out where to go, then just pick at random
        #else:
            #while True:
            #    cx, cy = self.get_map_pos()
            #    #print "x,y = " +str( [x,y]) +"    cx,cy = " +str( [cx,cy] )
            #    if x != cx or y != cy:
            #        break

        #TODO: if last random move was east, don't go west, etc
        r = randint(4)
        if   r < 1 and not self.level_map.is_wall(x, y +1):
            #self.rect.y += SCALE
            collision = self.move(0, SCALE)
            if not collision:
                if VERBOSE:
                    print "Monster.find_move() randomly going South"
                return
        if r < 2 and not self.level_map.is_wall(x, y -1):
            #self.rect.y -= SCALE
            collision = self.move(0, -SCALE)
            if not collision:
                if VERBOSE:
                    print "Monster.find_move() randomly going North"
                return
        if r < 3 and not self.level_map.is_wall(x +1, y):
            #self.rect.x += SCALE
            collision = self.move(SCALE, 0)
            if VERBOSE:
                if not collision:
                    print "Monster.find_move() randomly going East"
                return
        if r < 4 and not self.level_map.is_wall(x -1, y):
            #self.rect.x -= SCALE
            collision = self.move(-SCALE, 0)
            if not collision:
                if VERBOSE:
                    print "Monster.find_move() randomly going West"
                return

    def move(self, dx, dy):
        """ Try to move by dx or dy amount, backout the change if we hit another monster."""
        self.rect.x += dx
        self.change_x = dx

        self.rect.y += dy
        self.change_y = dy
        if VERBOSE:
            print "Monster.move: dx,dy = " +str([dx,dy])

        #print ("Monster.move: monsters = " + str(self.monsters) )
        collision = False
        if self.monsters:
            self.monsters.remove(self)
            collision = self.move_collision( self.monsters )
            self.monsters.add(self)
        else:
            if VERBOSE:
                print "Monster.move: No other monsters"
        if collision:
            self.rect.x -= dx
            self.change_x = 0

            self.rect.y -= dy
            self.change_y = 0
            if VERBOSE:
                print "Monster.move collision with monster detected"
        return collision
            

    def update(self):      # Monster
        """ Update the Monster position, etc """
        self.hit_decal.setv(self.hit_pts)
        if self.stun_level > 0:
            self.stun.next()
            self.image = self.stun.sprite
        else:
            self.image = self.base_image.copy()
            if self.resurection_cnt > 0:
                pygame.draw.line(self.image, YELLOW, (0,0), (32,32), 5) 
                pygame.draw.line(self.image, YELLOW, (0,32), (32,0), 5) 
        self.image.blit(self.hit_decal.image, (SCALE-self.hit_decal.w,SCALE-self.hit_decal.h) )  # Lower Right


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
        equipment = Equipment()
        self.equipment = equipment
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
                #print( "Player.use_equipment(): equipment = " +str(self.equipment) )
            if self.equipment.get(self.equip_loc):
                # If we got here, then the eqipment location is something other than none
                e = self.equipment.get(self.equip_loc)
                print( "Player.use_equipment(" +str(key) +"): equipment["+str(self.equip_loc) +"] = " +str(e) )
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
     
                # Decrement the equipment
                self.equipment.rm(self.equip_loc)
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
            if equip_loc < self.equipment.length():
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
                    self.equipment.add( block.e_type )
                    print self.equipment.get_list()

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
 
 
 
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, surf):
        """ Constructor for the wall that the player and monsters can run into. """
        super(Wall, self).__init__()
 
        ## Make a blue wall, of the size specified in the parameters
        #if name:
        #    #if os.path.isfile(name):
        #    #    #tile = pygame.image.load(name).convert_alpha()
        #    #    #self.image = pygame.image.load(name).convert()
        #    #    #self.image.blit(tile, (0,0) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)
        #    #else:
        #    #    self.image = pygame.Surface([SCALE, SCALE])
        #    #    self.image.fill(name)
        #else:
        self.image = surf
        #   self.image = pygame.Surface([SCALE, SCALE])
        #   self.image.fill(GRAY_37)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y*SCALE
        self.rect.x = x*SCALE

    def get_map_pos(self):
        return (self.rect.x / SCALE, self.rect.y / SCALE)

class Status(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, player, level, FONT): #, font):
        """ Constructor for the wall that the player and monsters can run into. """
        super(Status, self).__init__()
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.font = FONT
 
        #self.heart = pygame.image.load('images/heart.png').convert_alpha()
        self.heart = pygame.image.load('images/heart.png')
        #self.heart.set_alpha(255)

        #self.empty_heart = pygame.image.load('images/empty_heart.png').convert_alpha()
        self.empty_heart = pygame.image.load('images/empty_heart.png')

        self.equipment_images = []
        #for fname in PU_IMAGES:
        for n in range(len(E_DATA)):
            fname = E_DATA[n][E_IMAGE]
            if fname:
                #self.equipment_images.append( pygame.image.load(fname).convert_alpha() )
                self.equipment_images.append( pygame.image.load(fname) )
            else:
                self.equipment_images.append( None )


        self.player = player

        self.max_level = 4
        self.level_images = []
        for n in range(self.max_level):
            fname = 'images/level_' +str(n+1) +'.png'
            #self.level_images.append( pygame.image.load(fname).convert_alpha() )
            self.level_images.append( pygame.image.load(fname) )
        self.level=level
        #self.new_level()
        #self.image.blit(self.level_images[self.level], (x,y) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)

        self.update()

    def get_map_pos(self):
        return (self.rect.x / SCALE, self.rect.y / SCALE)

    #def new_level(self):
    #    self.image.blit(self.level_images[self.level], (x,y) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)
 
    def update(self):
        # Make a background
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(PURPLE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = self.y
        self.rect.x = self.x

        # Now draw Hearts for hit points on top of background
        #width = self.heart.get_size()[0] + 5
        width = 20
        y = 0
        for n in range(self.player.max_hit_pts):
            x = n * (width) 

            if n < self.player.hit_pts:
                self.image.blit(self.heart, (x,y) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)
            else:
                self.image.blit(self.empty_heart, (x,y) ) # area=None, special_flags = 0)
                #pygame.draw.circle(self.image, BLACK, (x,y), 5)

        # Draw Equipment
        width = 25
        if self.player.equip_loc != None:
            # Draw box around selected equipment
            n = self.player.equip_loc
            x = n * (width) +SCREEN_W/2 +width/2
            pygame.draw.rect(self.image, GRAY_37, (x+6,y+8, width, width) )
        for n in range(self.player.equipment.length()):
            # Draw the equipment storage boxes/locations
            x = n * (width) +SCREEN_W/2 +width/2
            pygame.draw.rect(self.image, PURPLE_DARK, (x+4,y+6, width-2, width-2) )
        for n in range( self.player.equipment.length() ):
            # Draw the equipment
            if self.player.equipment.get(n):
                x = n * (width) +SCREEN_W/2 +width/2
                self.image.blit(self.equipment_images[self.player.equipment.get(n)], (x,y) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)

        #self.level = self.player.level -1
        #if self.level > self.max_level -1:
        #    self.level = self.max_level -1
        #self.image.blit(self.level_images[self.level], (5, STATUS_H/2 -5) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)
        plevel_label = self.font.render("P:" +str(self.player.level), 1, GREENISH)
        self.image.blit(plevel_label, (20, STATUS_H/2) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)

        level_label = self.font.render("L:" +str(self.level), 1, GREENISH)
        self.image.blit(level_label, (SCREEN_W/3, STATUS_H/2) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)

        score_label = self.font.render(str(self.player.exp_pts), 1, GREENISH)
        self.image.blit(score_label, (2*SCREEN_W/3, STATUS_H/2) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)

class Ladder(pygame.sprite.DirtySprite):
    def __init__(self, start_pos):
        super(Ladder, self).__init__()
        self.image = pygame.image.load('images/ladder32.png')
        self.dirty = 2
        self.blendmode = 0
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = start_pos[1] * SCALE   # Note: rect is graphic position, not map position
        self.rect.x = start_pos[0] * SCALE   # Note: rect is graphic position, not map position
        self.pos = start_pos                 # None: this is MAP position
 
    def get_map_pos(self):
        return (self.rect.x / SCALE, self.rect.y / SCALE)

"""
class Level(pygame.sprite.Sprite):
 
    def __init__(self, x, y):
        super(Level, self).__init__()
        
        self.max_level = 4
        self.level_images = []
        for n in range(self.max_level):
            fname = 'images/level_' +str(n+1) +'.png'
            print ("Level.fname = " +fname)
            #self.level_images.append( pygame.image.load(fname).convert_alpha() )
            self.level_images.append( pygame.image.load(fname) )
        self.level=0
        self.new_level()
        self.image = self.level_images[self.level]
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.player = None
"""



