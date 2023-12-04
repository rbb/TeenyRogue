# TeenyRogue


This is a clone of an iOS game, TinyRogue. 

The original developer,  [Ravenous Games](http://ravenousgames.com), doesn't
seem to be maintaining it anymore. And their website doesn't seem to work.
[Here](https://mobilesyrup.com/2015/12/20/game-of-the-week-tiny-rogue-ultra-difficult-turn-based-combat/)
is an article describing it.

While the original ran on iOS, this is a Python version, that uses pygame.

The code is a bit of a mess at the moment. This was my first time making a game.
So the architecture of it is quite crap.

# Installation

    ```
    # Recommended: Create a virtual environment:
    python -m venv env
    . env/bin/activate

    # Install
    pip install -e .
    ```
    


# Original Game Notes


Monster     Exp Pts
-------     -------
Ghost          100
Troll          100
Skeleton       100
Fast Thing     100
Bomba          200
knight         250
rat             50
ladder          50

Level 2: <=1250
Level 3: >3350,  <=3450
Level 4: >5175,  <=5375

Level 2: <=800
Level 3: <=2100
Level 4: >5175,  <=5375


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

