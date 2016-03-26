import GameMap
import numpy as np

gm = GameMap.game_map()
print( gm.m )
print ("\n");

print ("------- edgewalls() ----------");
gm.setedges(1)
print( gm.m )
print ("\n");

print ("------- newrand() ----------");
gm.newrand()
print( gm.m )
print( gm.m.mean() )
print ("\n");

print ("------- clearpath() ----------");
gm.clearpath()
print( gm.m )
print( gm.m.mean() )
print ("\n");


print ("------- testwall() ----------");
print ( gm.testwall(0,0) )
print ( gm.testwall(gm.X-1,gm.Y-1) )
print ( gm.testwall(gm.X,gm.Y) )
print ("\n");


print ("------- randempty() ----------");
print ( gm.randempty() )
print ("\n");




print ("=========================================\n")

gm = GameMap.game_map(5,5)
gm.m = np.array([ [ 1,1,1,1,1],
                  [ 1,0,1,0,1],
                  [ 1,1,1,1,1],
                  [ 1,0,1,0,1],
                  [ 1,1,1,1,1] ])
print( gm.m )
print( gm.m.mean() )
print ("------- clearpath() ----------");
gm.clearpath()
print( gm.m )
print( gm.m.mean() )
print ("\n");
print ("\n");
