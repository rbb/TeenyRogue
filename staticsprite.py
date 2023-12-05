import pygame
# from pygame.locals import *
import numpy as np
import utils
# from decal import Decal

# Static sprites - ie ones that (for the most part) don't move around.


# Equipment (powerup) database
# Note: first entry is bogus so logic in Player.use_equipment() works
E_DATA = [
#        Image Name          Damage, ballistic, global, targeting, exp pts, Requires Slot
    [None,                      0,      False,   False,  False,      0,       True],   # noqa: E202 E241
    ["images/dagger32.png",     1,      True,    False,  False,      0,       True],   # noqa: E202 E241
    ["images/firebomb32.png",   2,      True,    False,  False,      0,       True],   # noqa: E202 E241
    ["images/firestorm32.png",  1,      False,   True,   False,      0,       True],   # noqa: E202 E241
    ["images/freezebomb32.png", 1,      True,    False,  False,      0,       True],   # noqa: E202 E241
    ["images/freeze32.png",     1,      False,   True,   False,      0,       True],   # noqa: E202 E241
    ["images/lightning32.png",  1,      False,   False,  True,       0,       True],   # noqa: E202 E241
    ["images/treasure32.png",   0,      False,   False,  False,     500,      False],  # noqa: E202 E241
]
E_NONE = 0     # Note: bogus entry for "No equpment"
E_DAGGER = 1
E_FIRE_BOMB = 2
E_FIRESTORM = 3
E_FREEZE_BOMB = 4
E_FREEZE_STORM = 5
E_LIGHTNING = 6
E_TREASURE = 7
# TODO other equipment
E_MAX = 8

E_IMAGE = 0
E_DAMAGE = 1
E_BALLISTIC = 2
E_GLOBAL = 3
E_TARGETING = 4
E_EXP_PTS = 5
E_SLOT = 6


class Equipment:
    def __init__(self):
        self.db = E_DATA
        self.e_type = None
        self.fname = None

    def rand_select(self):
        self.e_type = int(round(np.random.uniform(1, len(self.db) - 1)))
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
    # def __init__(self, starting_equip=[E_FIRESTORM, E_NONE, E_NONE, E_NONE]):   # DEBUG
    def __init__(self, starting_equip=[E_FREEZE_STORM, E_FREEZE_STORM, E_DAGGER, E_DAGGER]):   # DEBUG
    #def __init__(self, starting_equip=[E_DAGGER, E_NONE, E_NONE, E_NONE]):
        self.e_list = starting_equip
        self.db = E_DATA
        self.loc = None       # ie a slot number in e_list (0-3)

    def add(self, e):
        """Add an equipment item (e) to the equipment list, in the next empty slot.

           Return False if no slots exist or if equipment type being added is invalid."""
        # Verify e is a valid eqipment type
        if not self.valid(e):
            return False

        print(f"EquipmentList {e=}")

        if E_DATA[e][E_SLOT] == False:
            # if the item does not require a slot (Treasure)
            return True

        for n in range(self.length()):
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
            self.e_list.append(E_NONE)

    def get_e_type(self, n=None):
        if n is None:
            n = self.loc
        return self.e_list[n]

    def get_image_name(self, n=None):
        if n is None:
            n = self.loc
        return self.db[self.e_list[n]][E_IMAGE]

    def rm(self, n=None):
        if n is None:
            nrm = self.loc
        else:
            nrm = n
        print("EquipmentList.rm: n = " + str(nrm))
        if E_NONE != self.e_list[nrm]:
            self.e_list[nrm] = E_NONE
            return True
        else:
            return False
        if n is None:
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

    # def get_exp_pts(self):
    #    return self.db[self.e_type][E_EXP_PTS]

    def targeting(self, n=None):
        if n is None:
            n = self.loc
        if n > self.length():
            return False
        return self.db[self.e_list[n]][E_TARGETING]

    def global_area(self, n=None):
        if n is None:
            n = self.loc
        if n > self.length():
            return False
        return self.db[self.e_list[n]][E_GLOBAL]

    def ballistic(self, n=None):
        if n is None:
            n = self.loc
        if n > self.length():
            return False
        return self.db[self.e_list[n]][E_BALLISTIC]

    def damage(self, n=None):
        if n is None:
            n = self.loc
        if n > self.length():
            return False
        return self.db[self.e_list[n]][E_DAMAGE]


class Status(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, player, level, font):
        """ Constructor for the wall that the player and monsters can run into. """
        super(Status, self).__init__()
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.font = font

        # self.heart = pygame.image.load('images/heart.png').convert_alpha()
        self.heart = pygame.image.load('images/heart.png')
        # self.heart.set_alpha(255)

        # self.empty_heart = pygame.image.load('images/empty_heart.png').convert_alpha()
        self.empty_heart = pygame.image.load('images/empty_heart.png')

        self.equipment_images = []
        # for fname in PU_IMAGES:
        for n in range(len(E_DATA)):
            fname = E_DATA[n][E_IMAGE]
            if fname:
                # self.equipment_images.append(pygame.image.load(fname).convert_alpha())
                self.equipment_images.append(pygame.image.load(fname))
            else:
                self.equipment_images.append(None)

        self.player = player

        self.max_level = 4
        self.level_images = []
        for n in range(self.max_level):
            fname = f'images/level_{n + 1}.png'
            # self.level_images.append( pygame.image.load(fname).convert_alpha() )
            self.level_images.append(pygame.image.load(fname))
        self.level = level
        # self.new_level()
        # self.image.blit(self.level_images[self.level], (x,y) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)

        self.update()

    def get_map_pos(self):
        return (self.rect.x / utils.SCALE, self.rect.y / utils.SCALE)

    def prn(self):
        """print some basic (debug) info"""
        print("rect(x,y):" + str([self.rect.x, self.rect.y]))
        print("get_map_pos():" + str(self.get_map_pos()))

    # def new_level(self):
    #    self.image.blit(self.level_images[self.level], (x,y) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)

    def update(self):
        # Make a background
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(utils.PURPLE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = self.y
        self.rect.x = self.x

        # Now draw Hearts for hit points on top of background
        # width = self.heart.get_size()[0] + 5
        width = 20
        y = 0
        for n in range(self.player.max_hit_pts):
            x = n * width

            if n < self.player.hit_pts:
                self.image.blit(
                    self.heart,
                    (x, y),
                    # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)
                )
            else:
                self.image.blit(
                    self.empty_heart,
                    (x, y),
                    # area=None, special_flags = 0)
                )
                # pygame.draw.circle(self.image, BLACK, (x,y), 5)

        # Draw Equipment
        width = 25
        if self.player.equipmentl.loc is not None:
            # Draw box around selected equipment
            n = self.player.equipmentl.loc
            x = n * width + utils.SCREEN_W / 2 + width / 2
            pygame.draw.rect(self.image, utils.GRAY_37, (x + 6, y + 8, width, width))
        for n in range(self.player.equipmentl.length()):
            # Draw the equipmentl storage boxes/locations
            x = n * width + utils.SCREEN_W / 2 + width / 2
            pygame.draw.rect(
                self.image,
                utils.PURPLE_DARK,
                (x + 4, y + 6, width - 2, width - 2),
            )
        for n in range(self.player.equipmentl.length()):
            # Draw the equipmentl
            if self.player.equipmentl.get_e_type(n):
                x = n * width + utils.SCREEN_W / 2 + width / 2
                self.image.blit(
                    self.equipment_images[self.player.equipmentl.get_e_type(n)],
                    (x, y),
                    # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)
                )

        # self.level = self.player.level -1
        # if self.level > self.max_level -1:
        #    self.level = self.max_level -1
        # self.image.blit(self.level_images[self.level], (5, utils.STATUS_H/2 -5) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)
        plevel_label = self.font.render("P:" + str(self.player.level), 1, utils.GREENISH)
        self.image.blit(
            plevel_label,
            (20, utils.STATUS_H / 2)
            # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)
        )

        level_label = self.font.render("L:" + str(self.level), 1, utils.GREENISH)
        self.image.blit(
            level_label,
            (utils.SCREEN_W / 3, utils.STATUS_H / 2)
            # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)
        )

        score_label = self.font.render(str(self.player.exp_pts), 1, utils.GREENISH)
        self.image.blit(
            score_label,
            (2 * utils.SCREEN_W / 3, utils.STATUS_H / 2),
            # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)
        )


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, surf):
        """ Constructor for the wall that the player and monsters can run into. """
        super(Wall, self).__init__()

        # Make a blue wall, of the size specified in the parameters
        # if name:
        #    #if os.path.isfile(name):
        #    #    #tile = pygame.image.load(name).convert_alpha()
        #    #    #self.image = pygame.image.load(name).convert()
        #    #    #self.image.blit(tile, (0,0) ) # , area=self.heart.get_rect(), special_flags = BLEND_RGBA_ADD)
        #    #else:
        #    #    self.image = pygame.Surface([utils.SCALE, utils.SCALE])
        #    #    self.image.fill(name)
        # else:
        self.image = surf
        #   self.image = pygame.Surface([utils.SCALE, utils.SCALE])
        #   self.image.fill(utils.GRAY_37)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y * utils.SCALE
        self.rect.x = x * utils.SCALE

    def prn(self):
        """print some basic (debug) info about Wall sprites"""
        print("rect(x,y):" + str([self.rect.x, self.rect.y]))
        print("get_map_pos():" + str(self.get_map_pos()))

    def get_map_pos(self):
        return (self.rect.x / utils.SCALE, self.rect.y / utils.SCALE)


class Ladder(pygame.sprite.DirtySprite):
    def __init__(self, start_pos):
        super(Ladder, self).__init__()
        self.image = pygame.image.load('images/ladder32.png')
        self.dirty = 2
        self.blendmode = 0

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = start_pos[1] * utils.SCALE   # Note: rect is graphic position, not map position
        self.rect.x = start_pos[0] * utils.SCALE   # Note: rect is graphic position, not map position
        self.pos = start_pos                 # None: this is MAP position

    def prn(self):
        """print some basic (debug) info about Ladder sprites"""
        print("rect(x,y):" + str([self.rect.x, self.rect.y]))
        print("get_map_pos():" + str(self.get_map_pos()))

    def get_map_pos(self):
        return (self.rect.x / utils.SCALE, self.rect.y / utils.SCALE)


class DeadBanner():
    def __init__(self, player_level, map_level, score):
        self.font = pygame.font.SysFont("couriernew", 12, bold=True)
        self.banner = pygame.Surface([217, 307]) # TODO: get size from PNG
        #self.banner.fill(utils.PURPLE)
        self.banner.blit(
            pygame.image.load('images/dead.png'),
            (0, 0),
        )

        self.text("Congratulations!", (53, 92))
        self.text("You have died!", (58, 104))
        #banner.blit(
        #    dead_font.render(
        #        "You have died!", 1, utils.YELLOW),
        #    (51, 112),
        #)
        h = utils.SCREEN_H /2 - 30
        dh = 12
        self.text(f"Player Level:  {player_level}", (40, h))
        self.text(f"Dungeon Level: {map_level}", (40, h + dh))
        score_font = pygame.font.SysFont("couriernew", 20, bold=True)
        self.banner.blit(
            score_font.render("Score:", 1, utils.YELLOW),
            (75, 218),
        )
        score_x = 87
        if score >= 1000000:
            score_font = pygame.font.SysFont("couriernew", 14, bold=True)
            score_x = 70
        elif score >= 10000:
            score_font = pygame.font.SysFont("couriernew", 18, bold=True)
            score_x = 73
        elif score >= 1000:
            score_font = pygame.font.SysFont("couriernew", 18, bold=True)
            score_x = 80
        self.banner.blit(
            score_font.render(f"{score:,}", 1, utils.YELLOW),
            (score_x, 238),
        )
        self.text("Press Any Key to Quit",
                  (33, h + 4 * dh),
                  utils.RED,
        )
        return

    def text(self, s, pos, color=utils.YELLOW):
        self.banner.blit(
            self.font.render(s, 1, color), pos)
