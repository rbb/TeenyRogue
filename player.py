import pygame
import sys
# from pygame.locals import *
import utils
import mysprite
import staticsprite


class Player(mysprite.BaseSprite):
    """ Watcha Gon' Do Playa' """

    def __init__(self, start_pos):

        image = pygame.image.load('images/player32.png')
        super(Player, self).__init__(start_pos, image)

        # self.dx = self.image.get_size()[0]
        # self.dy = self.image.get_size()[1]

        self.max_hit_pts = 3
        self.hit_pts = 2
        self.damage = 1    # ability to do damage
        self.equipmentl = staticsprite.EquipmentList()
        self.level = 1
        self.powerups = None

        self.PM_MOVE = 0
        self.PM_BALLISTIC_SELECT = 1
        self.PM_BALLISTIC_FIRE = 2
        self.PM_TARGETING = 3
        self.PM_GLOBAL = 4
        self.mode = self.PM_MOVE

        self.ballistic = None

        # sprite groups
        self.monsters = None
        self.all_sprites = None
        self.ballistic_sprites = None
        self.n_target_monster = None

        # This is REALLY dumb. monsters is a sprite group, which is NOT iterable.
        # So, we need something that is iterable, to select a monster when targeting.
        #
        # From the pygame pages:
        #   sprites() -> sprite_list
        #   Return a list of all the Sprites this group contains. You can also
        #   get an iterator from the group, but you cannot iterator over a
        #   Group while modifying it.
        self.monster_list = None

        self.my_turn = True
        self.stun_rate = 2

        self.level_limits = [10000, 5200, 2000, 800]

    def drop_item(self):
        self.equipmentl.rm()
        self.mode = self.PM_MOVE

    # Player changepos()
    def changepos(self, key):
        # ---------------------------------------------------
        if self.key_is_equip(key):
            # Note this check is redundant if key_is_equip() is ALWAYS called first
            if not self.key_is_equip(key):
                return
            self.equipmentl.loc = key - pygame.K_1
            if utils.VERBOSE:
                print(f"Player.use_equipment({key}): equipmentl.loc = {self.equipmentl.loc}")
                # print( "Player.use_equipment(): equipmentl = " +str(self.equipmentl) )
            e = self.equipmentl.get_e_type()
            if e:
                # If we got here, then the eqipment location is something
                # other than none
                name = self.equipmentl.get_image_name()
                print(f"Player.use_equipment({key}): equipmentl[{self.equipmentl.loc}] = {e}, {name}")
                if self.equipmentl.ballistic():
                    self.mode = self.PM_BALLISTIC_SELECT
                    self.weapon = e
                elif self.equipmentl.targeting():
                    if len(self.monster_list) > 0:
                        self.mode = self.PM_TARGETING
                        self.weapon = e
                        self.n_target_monster = 0
                        self.monster_list[0].targeted = True
                        print(f"{self.n_target_monster=}")
                        print("Entering target mode")
                elif self.equipmentl.global_area():
                    self.mode = self.PM_GLOBAL
                    self.weapon = e
                    print("Entering Global Area mode")
            else:
                self.equipmentl.loc = None
        # ---------------------------------------------------
        if pygame.K_h == key:
            print("TODO: Help screen")
            print("")
            print("h       Print this help screen")
            print("arrows  Move, change target")
            print("1-4     Select equipment")
            print("return  Activate equipment")
            print("x       Drop equipment")
            print("j,k,l,i Move")
            print("k,i     Change target")
            print("e       Exit level (only if no monsters)")
            print("q       Quit")

        # ---------------------------------------------------
        if pygame.K_o == key:
            print("TODO: options screen")

        # ---------------------------------------------------
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
                # print(self.monsters)
                # print(len(self.monsters))
                if len(self.monsters) == 0:
                    # Note ladders is a sprite group, and can not be addressed as ldders[0]
                    for l in self.ladders:
                        self.change_x = l.rect.x - self.rect.x
                        self.change_y = l.rect.y - self.rect.y
                    print("exit to ladder:")
                    #print("   dx,dy  =: {self.dx},{self.dy}")
                    #print("   ladder =: {l.rect.x},[l.rect.y]")
                    #print("   change =: {self.change_x},{self.change_y}")
                    # self.my_turn = False
                else:
                    print(f"Shortcut to ladder not allowed, still {len(self.monster_list)} monsters left")
            elif pygame.K_d == key:
                print('Select eqipment item to drop first')

        # ---------------------------------------------------
        elif self.PM_BALLISTIC_SELECT == self.mode:
            if pygame.K_ESCAPE == key:
                self.mode = self.PM_MOVE
                self.weapon = None     # TODO: Do we need to define a mele weapon type??
                self.change_x = 0
                self.change_y = 0
                print("Returning to MOVE mode, from Ballistic mode")

            elif pygame.K_d == key:
                self.drop_item()

            elif self.key_is_move(key):
                ballistic_delta = 10
                ballistic_change_x = 0
                ballistic_change_y = 0
                if key == pygame.K_LEFT or (key == pygame.K_j):
                    ballistic_change_x = -ballistic_delta
                    print("my_ballistic LEFT")
                elif key == pygame.K_RIGHT or key == pygame.K_l:
                    ballistic_change_x = ballistic_delta
                    print("my_ballistic RIGHT")
                elif key == pygame.K_UP or key == pygame.K_i:
                    ballistic_change_y = -ballistic_delta
                    print("my_ballistic UP")
                elif key == pygame.K_DOWN or key == pygame.K_k:
                    ballistic_change_y = ballistic_delta
                    print("my_ballistic DOWN")

                self.my_ballistic = mysprite.Ballistic(
                    (self.rect.x, self.rect.y),
                    self.weapon, self.walls, self.monsters,
                    ballistic_change_x, ballistic_change_y, self)
                self.ballistic_sprites.add(self.my_ballistic)
                self.my_ballistic.prn()

                # Decrement the equipmentl
                self.equipmentl.rm()

                # Cleanup
                self.mode = self.PM_BALLISTIC_FIRE
                self.weapon = None     # TODO: Do we need to define a mele weapon type??
                print("Transitioning to FIRE mode")

        # ---------------------------------------------------
        elif self.PM_BALLISTIC_FIRE == self.mode:
            # self.ballistic.update()
            pass

        # ---------------------------------------------------
        elif self.PM_TARGETING == self.mode:
            # TODO: figure out keys (or mouse) for targeting: maybe 'n','p' for next,prev; and 'return' for commit?
            print("Player Target Mode")
            if pygame.K_d == key:
                self.drop_item()

            elif pygame.K_ESCAPE == key:
                print("n_targeted_monster = " + str(self.n_target_monster))
                self.mode = self.PM_MOVE
                self.weapon = None     # TODO: Do we need to define a mele weapon type??
                self.equipmentl.loc = None
                if self.n_target_monster is not None:
                    self.monster_list[self.n_target_monster].targeted = False
                    print(f"Disabling targeted monster {self.n_target_monster}")
                self.n_target_monster = None
                print("Returning to MOVE mode, from target mode")

            elif key in [pygame.K_j, pygame.K_k, pygame.K_DOWN, pygame.K_UP]:
                N = len(self.monster_list)
                print("Targeting N monsters = " + str(N))
                if N == 0:
                    self.mode = self.PM_MOVE
                    self.weapon = None     # TODO: Do we need to define a mele weapon type??
                    self.n_target_monster = None
                    print("Returning to MOVE mode, targeting found no monsters")
                if pygame.K_k == key or pygame.K_DOWN == key:
                    if self.n_target_monster is None:
                        self.n_target_monster = 0
                    else:
                        self.monster_list[self.n_target_monster].targeted = False
                        if self.n_target_monster == N - 1:
                            self.n_target_monster = 0
                        else:
                            self.n_target_monster += 1
                    self.monster_list[self.n_target_monster].targeted = True
                    print(f"Targeting (down) selected monster {self.n_target_monster}")
                if pygame.K_i == key or pygame.K_UP == key:
                    if self.n_target_monster is None:
                        self.n_target_monster = N - 1
                    else:
                        self.monster_list[self.n_target_monster].targeted = False
                        if self.n_target_monster == N - 1:
                            self.n_target_monster = N - 1
                        else:
                            self.n_target_monster -= 1
                    self.monster_list[self.n_target_monster].targeted = True
                    print(f"Targeting (up) selected monster {self.n_target_monster}")

            elif pygame.K_RETURN == key:
                if self.n_target_monster is not None:
                    # self.monster_list[self.n_target_monster].targeted = False
                    print(f"Disabling targeted monster {self.n_target_monster}")
                    monster = self.monster_list[self.n_target_monster]
                    self.do_damage(monster, 0, self.equipmentl.damage()) # no stun
                    self.mode = self.PM_MOVE
                    self.weapon = None     # TODO: Do we need to define a mele weapon type??
                    self.n_target_monster = None

                    # Decrement the equipmentl
                    self.equipmentl.rm()

        # ---------------------------------------------------
        elif self.PM_GLOBAL == self.mode:
            # TODO: figure out keys (or mouse) for targeting: maybe 'n','p' for next,prev; and 'return' for commit?
            print("Player Global Area Mode")
            if pygame.K_d == key:
                self.drop_item()

            elif pygame.K_ESCAPE == key:
                self.mode = self.PM_MOVE
                self.weapon = None     # TODO: Do we need to define a mele weapon type??
                self.equipmentl.loc = None
                print("Returning to MOVE mode, from target mode")

            elif pygame.K_RETURN == key:
                # Since the monster_list gets modified inside do_damage(), we
                # can't just do a for loop.
                n = 0
                while n < len(self.monster_list):
                    print(f"Monster {n}, {self.monster_list[n].fname}")
                    monster = self.monster_list[n]
                    if self.do_damage(monster, 0, self.equipmentl.damage()):  # no stun
                        # the current monster was removed from the list
                        pass
                    else:
                        n += 1

                self.mode = self.PM_MOVE
                self.weapon = None     # TODO: Do we need to define a mele weapon type??

                # Decrement the equipmentl
                self.equipmentl.rm()
        # ---------------------------------------------------
        else:
            print("Unknown Player Mode")
            sys.exit(0)

    def key_is_move(self, key):
        # TODO: Use w,a,s,d like arrow keys. Use h,j,k,l like vim
        if key in [pygame.K_LEFT, pygame.K_j,
                   pygame.K_RIGHT, pygame.K_l,
                   pygame.K_UP, pygame.K_i,
                   pygame.K_DOWN, pygame.K_k]:
            return True
        else:
            return False

    def key_is_target_select(self, key):
        # TODO: Use w,a,s,d like arrow keys. Use h,j,k,l like vim
        if key in [pygame.K_UP, pygame.K_i, pygame.K_DOWN]:
            return True
        else:
            return False

    def key_is_equip(self, key):
        if key >= pygame.K_1 and key <= pygame.K_9:
            self.equipmentl.loc = key - pygame.K_1
            if self.equipmentl.loc < self.equipmentl.length():
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
                    if self.do_damage(block, self.stun_rate):
                        block.kill()

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

            # Check and see if we hit the ladder
            block_hit_list = pygame.sprite.spritecollide(self, self.ladders, False)
            for block in block_hit_list:
                # Complete the level
                self.kill()

            self.change_x = 0
            self.change_y = 0

            if self.powerups:  # TODO require powerups as part of __init__(), so we don't need this test?
                block_hit_list = pygame.sprite.spritecollide(self, self.powerups, False)
                for block in block_hit_list:
                    if self.equipmentl.add(block.equip.e_type):
                        self.exp_pts += block.exp_pts
                        if utils.VERBOSE:
                            print(f"adding {block.exp_pts} exp pts from powerup etype = {block.e_type}")
                        #pygame.sprite.spritecollide(self, pygame.sprite.Group(block), True)
                        self.powerups.remove(block)
                    else:
                        if utils.VERBOSE:
                            print(f"Failed to Add {block.exp_pts} exp pts from powerup etype = {block.e_type}")
                    print(self.equipmentl.get_list())

        elif self.PM_BALLISTIC_SELECT == self.mode:
            pass

        elif self.PM_BALLISTIC_FIRE == self.mode:
            if not self.my_ballistic.alive():  # Poor nomenclature, it means the sprite is not on the screen
                if self.my_ballistic.exp_pts > 0:
                    # Monster exp pts were transferred to the ballistic. Here we transfer to player
                    self.add_exp_pts(self.my_ballistic.exp_pts)
                    print("Dead Monster worth " + str(self.my_ballistic.exp_pts) + " points")
                    print("Player killed Monster with my_ballistic. now at " + str(self.exp_pts) + " points")
                self.my_ballistic = None
                self.mode = self.PM_MOVE
                self.weapon = None     # TODO: Do we need to define a mele weapon type??
                print("Player.update(): my_ballistic hit something. Returning to MOVE mode")
                self.my_turn = False

        elif self.PM_TARGETING == self.mode:
            pass
        # print("Player.update complete")

    def add_exp_pts(self, pts):
        self.exp_pts += pts
        N = len(self.level_limits)
        for n in range(N):
            if self.exp_pts > self.level_limits[n]:
                if utils.VERBOSE:
                    print(f"add_exp_pts: {self.exp_pts=}  > level_limits[{n}] = {self.level_limits[n]}")
                self.level = (N - n) + 1
                break

    def do_damage(self, monster, stun_rate, damage=None):
        "Return True if monster was killed"
        if damage is None:
            damage = self.damage
        monster.wound(self.damage, stun_rate)
        monster.targeted = False
        if monster.hit_pts <= 0:
            if monster.not_dead_yet or monster.resurection_pts == 0:
                # Note: not_dead_yet, used to prevent resurected monsters from providing additional exp pts
                self.add_exp_pts(monster.exp_pts)
                print("Dead Monster worth " + str(monster.exp_pts) + " points")
                monster.not_dead_yet = False
                print("Player killed Monster. now at " + str(self.exp_pts) + " exp points")
                if monster.resurection_pts == 0:
                    print("Dead targeted Monster, cleaning up.")
                    self.monsters.remove(monster)
                    for n in range(len(self.monster_list)):
                        if self.monster_list[n] == monster:
                            del self.monster_list[n]
                            break
                    monster.kill()
                    return True
        return False

    def print_state(self):
        print("Player: print_state()")

        print("powerups:")
        print("---------")
        for p in self.powerups:
            p.prn()
        print("")

        print("all_sprites:")
        print("-------------")
        for p in self.all_sprites:
            print(str([p.rect.x, p.rect.y]) + ", " + str(p.get_map_pos()))
        print("")

        print("ballistic_sprites:")
        print("------------------")
        for p in self.ballistic_sprites:
            p.prn()
        print("")

        if self.monsters:
            print("monsters:")
            print("-------------")
            for p in self.monsters:
                p.prn()
            print("")
