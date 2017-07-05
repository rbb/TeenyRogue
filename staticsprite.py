import pygame, sys
from pygame.locals import *
import numpy as np
from utils import *
import os
import time
from decal import Decal

# Static sprites - ie ones that (for the most part) don't move around.


# Equipment (powerup) database
#             Image Name          Damage, ballistic, global, targeting, exp pts
E_DATA = [[None,                     0,      False,   False,  False,      0 ], # Note: first entry is bogus so logic in Player.use_equipment() works
          ["images/dagger32.png",    1,      True,    False,  False,      0 ],
          ["images/firebomb32.png",  2,      True,    False,  False,      0 ],
          ["images/firestorm32.png", 1,      False,   True,   False,      0 ],
          ["images/freezebomb32.png",1,      True,    False,  False,      0 ],
          ["images/freeze32.png",    1,      False,   True,   False,      0 ],
          ["images/lightning32.png", 1,      False,   False,  True,       0 ],
          ["images/treasure32.png",  0,      False,   False,  False,     500] ]
E_NONE = 0     # Note: bogus entry for "No equpment"
E_DAGGER = 1
E_FIRE_BOMB = 2
E_FIRESTORM = 3
E_FREEZE_BOMB = 4
E_FREEZE_STORM = 5
E_LIGHTNING = 6
# TODO other equipment
E_MAX = 6

E_IMAGE = 0
E_DAMAGE = 1
E_BALLISTIC = 2
E_GLOBAL = 3
E_TARGETING = 4
E_EXP_PTS = 5

class Equipment:
    def __init__(self):
        self.db = E_DATA
        self.e_type = None
        self.fname = None

    def rand_select(self):
        self.e_type = int(round( np.random.uniform(1, len(self.db)-1) ))
        return self.e_type

    def image_fname(self):
        self.fname = self.db[self.e_type][E_IMAGE]
        return self.fname

    def get_damage(self):
        return self.db[self.e_type][E_DAMAGE]

    def get_exp_pts(self):
        return self.db[self.e_type][E_EXP_PTS]

    def targeting(self):
        return self.db[self.e_type][E_TARGETING]

    def global_area(self):
        return self.db[self.e_type][E_GLOBAL]

    def ballistic(self):
        return self.db[self.e_type][E_BALLISTIC]
        

class EquipmentList:
    """A player's equipment list"""
    #def __init__(self, starting_equip=[E_DAGGER, E_NONE, E_NONE, E_NONE]):
    #def __init__(self, starting_equip=[E_FIRESTORM, E_NONE, E_NONE, E_NONE]):   # DEBUG
    def __init__(self, starting_equip=[E_FIRESTORM, E_DAGGER, E_NONE, E_NONE]):   # DEBUG
        self.e_list = starting_equip
        self.db = E_DATA
        self.loc = None       # ie a slot number in e_list (0-3)

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

    def get_e_type(self, n=None):
        if n == None:
            n = self.loc
        return self.e_list[n]

    def rm(self, n=None):
        if n == None:
            nrm = self.loc
        else:
            nrm = n
        print "EquipmentList.rm: n = " +str(nrm)
        if E_NONE != self.e_list[nrm]:
            self.e_list[nrm] = E_NONE
            return True
        else:
            return False
        if n == None:
            self.loc = None

    def get_list(self):
        return self.e_list

    def n_items(self):
        n = 0
        for e in self.e_list:
            if e:
                n += 1
        return n

    def length(self):
        return len(self.e_list)

    #def get_exp_pts(self):
    #    return self.db[self.e_type][E_EXP_PTS]

    def targeting(self, n=None):
        if n == None:
            n = self.loc
        if n > self.length():
            return False
        return self.db[self.e_list[n]][E_TARGETING]

    def global_area(self, n=None):
        if n == None:
            n = self.loc
        if n > self.length():
            return False
        return self.db[self.e_list[n]][E_GLOBAL]

    def ballistic(self, n=None):
        if n == None:
            n = self.loc
        if n > self.length():
            return False
        return self.db[self.e_list[n]][E_BALLISTIC]

    def damage(self, n=None):
        if n == None:
            n = self.loc
        if n > self.length():
            return False
        return self.db[self.e_list[n]][E_DAMAGE]

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
        if self.player.equipmentl.loc != None:
            # Draw box around selected equipment
            n = self.player.equipmentl.loc
            x = n * (width) +SCREEN_W/2 +width/2
            pygame.draw.rect(self.image, GRAY_37, (x+6,y+8, width, width) )
        for n in range(self.player.equipmentl.length()):
            # Draw the equipmentl storage boxes/locations
            x = n * (width) +SCREEN_W/2 +width/2
            pygame.draw.rect(self.image, PURPLE_DARK, (x+4,y+6, width-2, width-2) )
        for n in range( self.player.equipmentl.length() ):
            # Draw the equipmentl
            if self.player.equipmentl.get_e_type(n):
                x = n * (width) +SCREEN_W/2 +width/2
                self.image.blit(self.equipment_images[self.player.equipmentl.get_e_type(n)], (x,y) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)

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

