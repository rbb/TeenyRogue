import GameMap
import numpy as np

gm = GameMap.game_map(5,10)
gm.prn()
print ("\n");

print ("------- edgewalls() ----------");
gm.setedges(0)
gm.prn()
gm.setedges(1)
gm.prn()
print ("\n");


print ("------- newrand() ----------");
gm.newrand()
gm.prn()
print( gm.m.mean() )
print ("\n");

print ("------- clearpath() ----------");
gm.clearpath()
gm.prn()
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
gm.prn()
print( gm.m.mean() )
print ("------- clearpath() ----------");
gm.clearpath()
gm.prn()
print( gm.m.mean() )
print ("\n");
print ("\n");

print ("=========================================\n")
gm = GameMap.game_map(5,6)
gm.m = np.array([ [ 1,1,1,1,1],
                  [ 1,0,1,0,1],
                  [ 1,1,1,1,1],
                  [ 1,0,1,0,1],
                  [ 1,1,1,1,1],
                  [ 1,1,1,1,1] ])
gm.prn()
print "shape = " +str(gm.m.shape)
print "valid_path(1,1, 4,1) = " +str( gm.valid_path(1,1,4,1) )
#print "the non-valid map shows up as " +str(gm.valid())
print ("\n");

gm = GameMap.game_map(5,5)
gm.m = np.array([ [ 1,1,1,1,1],
                  [ 1,0,1,0,1],
                  [ 1,0,1,0,1],
                  [ 1,0,0,0,1],
                  [ 1,1,1,1,1] ])
gm.prn()
print "valid_path(1,1, 1,2) = " +str( gm.valid_path(1,1,1,2) )
print "valid_path(1,1, 4,1) = " +str( gm.valid_path(1,1,4,1) )
#print "the non-valid map shows up as " +str(gm.valid())

