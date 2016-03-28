import pygame, sys
from pygame.locals import *
import numpy as np
from utils import *



class BaseSprite(pygame.sprite.Sprite):
    """Base class for Monsters, Powerups, Player"""
 
    # Constructor function
    def __init__(self, start_pos, image):
        super(BaseSprite, self).__init__()
        self.image = image 
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = start_pos[1] * SCALE   # Note: rect is graphic position, not map position
        self.rect.x = start_pos[0] * SCALE   # Note: rect is graphic position, not map position
 
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        #self.dx = self.image.get_size()[0]
        #self.dy = self.image.get_size()[1]
        self.dx = SCALE
        self.dy = SCALE
        self.walls = None

        self.hit_pts = 1
        self.damage = 1    # ability to do damage
        self.equipment = None
        self.exp_pts = 0
 
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

    def update(self):
        pass
 

    """
    def collide(self, sprite_group, callback):
        # Move left/right
        self.rect.x += self.change_x
 
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, sprite_group, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, sprite_group, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
    """


class Powerup(BaseSprite):
    """ Powerups that the player can grab"""

    def __init__(self, start_pos, pu_type=None):
        # Call the parent's constructor
 
        PU_IMAGES = ["images/dagger32.png", "images/firebomb32.png", "images/firestorm32.png", 
                     "images/freeze32.png", "images/lightning32.png" ]
        #print (str(PU_IMAGES) )
        if (pu_type == None):
            self.pu_type = int(round( np.random.uniform(0, len(PU_IMAGES)-1) ))
        else:
            self.pu_type = pu_type
        fname = PU_IMAGES[ self.pu_type ] 
        image = pygame.image.load( fname )
        super(Powerup, self).__init__(start_pos, image)

class Monster(BaseSprite):
    """ Monsters. Need I say more? """
 
    def __init__(self, start_pos, m_type=None):
        #image = pygame.image.load('images/knight32.png')
        #super(Monster, self).__init__(start_pos, image)
        #BaseSprite.__init__(self, start_pos, image)

        if (m_type == None):
            self.m_type = int(round( np.random.uniform(0, len(M_DATA)-1) ))
        else:
            self.m_type = m_type
        fname = M_DATA[self.m_type][M_IMAGE_FNAME] 
        self.hit_pts = M_DATA[self.m_type][M_HIT_PTS] 
        self.moves = M_DATA[self.m_type][M_MOVES] 
        self.wall_stop = M_DATA[self.m_type][M_WALL_STOP] 
        self.ballistic = M_DATA[self.m_type][M_BALLISTIC] 
        self.exp_pts = M_DATA[self.m_type][M_EXP_PTS] 
        if VERBOSE:
            print ("Monster.fname = " +str(fname) )
        image = pygame.image.load( fname )
        super(Monster, self).__init__(start_pos, image)

    #def __getattr__(self, name):
    #    return getattr(self.BaseSprite, name)
 
    #def changepos(self, key):
    #    self.change_x = 0
    #    self.change_y = 0
    #    #TODO: figure out where the player is, and head there
    #    #TODO: Maybe modify the above behavior based on Monster type
 
    def update(self):
        """ Update the position, etc """
        # Move left/right
        self.rect.x += self.change_x
 
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
        self.change_x = 0
        self.change_y = 0


class Player(BaseSprite):
    """ Watcha Gon' Do Playa' """
 
    def __init__(self, start_pos):
 
        image = pygame.image.load('images/player32.png')
        super(Player, self).__init__(start_pos, image)
 
        #self.dx = self.image.get_size()[0]
        #self.dy = self.image.get_size()[1]

        self.max_hit_pts = 3
        self.hit_pts = 3
        self.damage = 1    # ability to do damage
        self.equipment = [E_DAGGER]
        self.level = 1
 
    def changepos(self, key):
        self.change_x = 0
        self.change_y = 0
        if key == pygame.K_LEFT:
            self.change_x = -self.dx
        elif key == pygame.K_RIGHT:
            self.change_x = self.dx
        elif key == pygame.K_UP:
            self.change_y = -self.dy
        elif key == pygame.K_DOWN:
            self.change_y = self.dy
 
    def update(self):
        """ Update the player position. """
        # Move left/right
        self.rect.x += self.change_x
 
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
        self.change_x = 0
        self.change_y = 0
 
 
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player and monsters can run into. """
        super(Wall, self).__init__()
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def get_map_pos(self):
        return (self.rect.x / SCALE, self.rect.y / SCALE)

    #def update(self):
    #    super(Wall, self).update()
 
class Status(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, player): #, font):
        """ Constructor for the wall that the player and monsters can run into. """
        super(Status, self).__init__()
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        #self.font = font
 
        self.heart = pygame.image.load('images/heart.png').convert_alpha()
        #self.heart = self.heart.convert_alpha()
        #self.heart.set_alpha(255)

        self.empty_heart = pygame.image.load('images/empty_heart.png')
        self.empty_heart = self.empty_heart.convert_alpha()

        self.player = player
        self.update()

    def get_map_pos(self):
        return (self.rect.x / SCALE, self.rect.y / SCALE)

    def update(self):
        #super(Status, self).update()
        # Make a background
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(PURPLE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = self.y
        self.rect.x = self.x

        # Now draw Hearts for hit points on top of background
        width = self.heart.get_size()[0] + 5
        for n in range(self.player.max_hit_pts):
            x = n * (width) + 10
            y = 10 #5

            #TODO: For some reason blitting images onto the background surface looks like shit
            if n <= self.player.hit_pts:
                #self.image.blit(self.heart, (x,y) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)
                pygame.draw.circle(self.image, RED, (x,y), 5)
            else:
                #self.image.blit(self.empty_heart, (x,y) ) # area=None, special_flags = 0)
                pygame.draw.circle(self.image, BLACK, (x,y), 5)

        #label = myfont.render(str(self.player.level), 1, GREENISH)

class Ladder(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super(Ladder, self).__init__()
        self.image = pygame.image.load('images/ladder32.png')
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = start_pos[1] * SCALE   # Note: rect is graphic position, not map position
        self.rect.x = start_pos[0] * SCALE   # Note: rect is graphic position, not map position
 
    def get_map_pos(self):
        return (self.rect.x / SCALE, self.rect.y / SCALE)

    #def update(self):
    #    super(Wall, self).update()
 
class Level(pygame.sprite.Sprite):
    """ Monsters. Need I say more? """
 
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

    def new_level(self):
        self.image = self.level_images[self.level]
 
    #def update(self):
        #if self.player:
        #    if self.level != self.player.level -1:
        #        self.level = self.player.level -1
        #        if self.level > self.max_level -1:
        #            self.level = self.max_level -1
        #        self.new_level()


