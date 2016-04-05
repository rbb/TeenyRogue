import GameMap
import numpy as np

gm = GameMap.game_map(5,10)
gm.prn_m()
print ("\n");

print ("------- edgewalls() ----------");
gm.setedges(0)
gm.prn_m()
gm.setedges(1)
gm.prn_m()
print ("\n");


print ("------- newrand() ----------");
gm.newrand()
gm.prn_m()
print( gm.m.mean() )
print ("\n");

print ("------- clearpath() ----------");
gm.clearpath()
gm.prn_m()
print( gm.m.mean() )
print ("\n");


print ("------- is_wall() ----------");
print ( gm.is_wall(0,0) )
print ( gm.is_wall(gm.X-1,gm.Y-1) )
print ( gm.is_wall(gm.X,gm.Y) )
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
gm.prn_m()
print( gm.m.mean() )
print ("------- clearpath() ----------");
gm.clearpath()
gm.prn_m()
print( gm.m.mean() )
print ("\n");
print ("\n");

print ("=========================================\n")
#gm = GameMap.game_map(5,6)
#gm.m = np.array([ [ 1,1,1,1,1],
#                  [ 1,0,1,0,1],
#                  [ 1,1,1,1,1],
#                  [ 1,0,1,0,1],
#                  [ 1,1,1,1,1],
#                  [ 1,1,1,1,1] ])
#gm.prn_m()
#print "shape = " +str(gm.m.shape)
#print "valid_path(1,1, 4,1) = " +str( gm.valid_path(1,1,4,1) )
##print "the non-valid map shows up as " +str(gm.valid())
#print ("\n");

gm = GameMap.game_map(5,5)
gm.m = np.array([ [ 1,1,1,1,1],
                  [ 1,0,1,0,1],
                  [ 1,1,1,0,1],
                  [ 1,0,0,0,1],
                  [ 1,1,1,1,1] ])

# The expected output
valid =np.array([ [ 1,1,1,1,1],
                  [ 1,1,1,0,1],
                  [ 1,1,1,0,1],
                  [ 1,0,0,0,1],
                  [ 1,1,1,1,1] ], int)
ret_valid = gm.is_valid()
print "is_valid() returns: " +str(ret_valid)
if np.all(False == ret_valid):
    print "is_valid() correct return"
else:
    print "is_valid() ERROR"


print "Expected gm.valid state"
gm.prn(valid)
print""
print "Test map output"
gm.prn_m()
print""
print "Actual gm.valid() state"
gm.prn_valid()

if np.all(gm.valid == valid):
    print "gm.valid state correct"
else:
    print "gm.valid state ERROR"

