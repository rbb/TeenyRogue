
Tasks
-------------------------
* Fix moving into walls lets monsters move
o targeting mechanism for non-ballistic powerups
   - highlight selected monster
   - inflict the damage
- Highlight selected powerups (ie when in targeting or ballistic mode, show the powerup selected)
- Leveling up
   - Graphics
   - Level up bonuses
- Improve hit points to level array accuracy
- Improve monster AI 
   - Ghosts should prefer going into walls
   - Shooters shoud perfer to not line up with player, or maybe at 50% chance?
- Torches on walls
- Original or free artwork for sprites
* blit hit points of monters on their sprites
- Flash screen on hits
- 'E' When no monsters goes to ladder
- Change sprites when they are stunned
- show levelup bonus status (ie vampire, +damage on firestorm, etc)
- zombie monsters (ie skeletons)
   - should not continue to take damage, until they re-animate
   * Allow player to walk over zombie monsters (ie skeletons)
- Daggers should be 3, and show count in equipment status
- Refactor, so that there is some sort of world state variable that can be passed around, 
  instead of putting a bunch of stuff in the 'player' variable
- Use 'p' key to print current game state?
- Fix monsters going through diagnal walls
   - Original doesn't seem to have diagnal walls, always a right angle
   - Maybe just skip levels generated with diagonal walls?
- Fix monsters going into walls (only at edges)????
- Animate each monster/player move
   - Maybe add a half tile frame?
- Implement "Bomba" (ballistic monsters) firing.
- Prevent monsters from being on ladder

Ghost 100
Troll 100
Skeleton 100
Fast Thing 100
Bomba 200
knight 250
rat 50
ladder 50

Level 2: <=1250
Level 3: >3350,  <=3450
Level 4: >5175,  <=5375

Level 2: <=800
Level 3: <=2100
Level 4: >5175,  <=5375

Congratulations! You Have Died
Quest Completed
Enemies Killed
Treasures Found
Dungeon Level
Hero Level
Total Score (exp pts)

fast, rat 200
ghost, fast, troll 550
fast, skel 750 lvl2, rat 800
Ghost, Rat, Troll 1150
fast, troll 1350, chest 1850, 1900
skel, skel, skel 2300 lvl3, 2350
Troll, troll, troll 2800
Ghost, fast, fast, 3450
skel, bomb, knight, 4050
knight 4300, rat +75, bomba, troll 150, 4775
chest 5225, bomba, troll, fast 5875
enemies = 38, level = 4

