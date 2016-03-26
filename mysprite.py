import pygame, sys
from pygame.locals import *
#import numpy as np



class BaseSprite(pygame.sprite.Sprite):
    """ Monsters. Need I say more? """
 
    # Constructor function
    def __init__(self, start_pos, image):
        # Call the parent's constructor
        super(BaseSprite, self).__init__()
 
        self.image = image 
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = start_pos[1]
        self.rect.x = start_pos[0]
 
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.dx = self.image.get_size()[0]
        self.dy = self.image.get_size()[1]
        self.walls = None
 
    def changepos(self, key):
        self.change_x = 0
        self.change_y = 0
        if key == pygame.K_LEFT:
            player.change_x = -self.dx
        elif key == pygame.K_RIGHT:
            player.change_x = self.dx
        elif key == pygame.K_UP:
            player.change_y = -self.dy
        elif key == pygame.K_DOWN:
            player.change_y = self.dy

 

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


class Monster(BaseSprite):
    """ Monsters. Need I say more? """
 
    # Constructor function
    def __init__(self, start_pos):
        # Call the parent's constructor
        super(Monster, self).__init__()
 
        # Set height, width
        #self.image = pygame.Surface([15, 15])
        #self.image.fill(WHITE)
        self.image = pygame.image.load('knight_32.png')
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = start_pos[1]
        self.rect.x = start_pos[0]
 
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.dx = self.image.get_size()[0]
        self.dy = self.image.get_size()[1]
        self.walls = None
 
    def changepos(self, key):
        self.change_x = 0
        self.change_y = 0
        if key == pygame.K_LEFT:
            player.change_x = -self.dx
        elif key == pygame.K_RIGHT:
            player.change_x = self.dx
        elif key == pygame.K_UP:
            player.change_y = -self.dy
        elif key == pygame.K_DOWN:
            player.change_y = self.dy
 
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


class Player(BaseSprite):
    """ Watcha Gon' Do Playa' """
 
    # Constructor function
    def __init__(self, start_pos):
        # Call the parent's constructor
        super(Player, self).__init__()
 
        # Set height, width
        #self.image = pygame.Surface([15, 15])
        #self.image.fill(WHITE)
        self.image = pygame.image.load('images/knight32.png')
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = start_pos[1]
        self.rect.x = start_pos[0]
 
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.dx = self.image.get_size()[0]
        self.dy = self.image.get_size()[1]
        self.walls = None
 
    def changepos(self, key):
        self.change_x = 0
        self.change_y = 0
        if key == pygame.K_LEFT:
            player.change_x = -self.dx
        elif key == pygame.K_RIGHT:
            player.change_x = self.dx
        elif key == pygame.K_UP:
            player.change_y = -self.dy
        elif key == pygame.K_DOWN:
            player.change_y = self.dy
 
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
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super(Wall, self).__init__()
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 

class Powerup(pygame.sprite.Sprite):
    """ Powerups that the player can grab"""
    def __init__(self, start_pos, pu_type=None):
        # Call the parent's constructor
        super(Powerup, self).__init__()
 
        #PU_IMAGES = ["images/lightning32.png", "images/sword.png"]
        PU_IMAGES = ["foo", "bar"]
        print (str(PU_IMAGES) )
        if (self.pu_type) == None or (self.pu_type > len(PU_IMAAGES) -1):
            self.pu_type = int(round(np.random.uniform(0, len(pu_images)-1)
        fname = PU_IMAGES[ self.pu_type ] 
        self.image = pygame.image.load( fname )

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = start_pos[1]
        self.rect.x = start_pos[0]
 
