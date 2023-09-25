import os
import json
import random
import sys
import math
from scripts.dirClass import Directory
from scripts.mapClass import HexMap as Map ## only hexmaps supported as of now
from scripts.layerClass import Layer
from scripts.paths import Paths
from scripts.defaults import Defaults


print("\nLets make maps!")

filename, mapx, mapy, tilex, tiley = Defaults.fillDefaultValues(sys.argv)

overwrite = Defaults.overwrite()
map = Map(filename)
if (overwrite == False):
    map.loadMap() ## Does nothing if a file under filename(.tmj) not found in maps folder
    if map.getData() == None:
        map.newEmptyMap(mapx, mapy, tilex, tiley)
else:
    map.newEmptyMap(mapx, mapy, tilex, tiley)

## Add relevant Tilesets
map.addTileSet("Init")

## Create the init layer, if map has one load that / if not initialize new one by said name
init_layer = map.findLayer("Init")
if init_layer == None:
    init_layer = Layer("Init")

##ocean 3 tiles from every direction
for tile in Layer.getTilesBorderXYSelect([0,0],[mapx-1,mapy-1]):
    init_layer.setTileAt(tile,1)
for tile in Layer.getTilesBorderXYSelect([1,1],[mapx-2,mapy-2]):
    init_layer.setTileAt(tile,2)
for tile in Layer.getTilesBorderXYSelect([2,2],[mapx-3,mapy-3]):
    init_layer.setTileAt(tile,3)



## Area that can be other stuff than the border ocean
generateableArea = Layer.getTilesBoxSelect([3,3],[mapx-4,mapy-4])
generateableTiles = len(generateableArea)
#working area XY starts and ends
waXs, waYs, waXe, waYe = 3,3,(mapx-4),(mapy-4)
landPercentage = Defaults.landPercentage()

#non constant values
landTiles = (math.floor(landPercentage/100*generateableTiles)) ##6185 
oceanTiles = generateableTiles-landTiles ##2651


"""
### Iterate from the outside in
rings=math.floor(min(waXe,waYe)/2)
for ring in range(rings):
    #with every loop increase the starting xy and decrease ending xy thus iterating the area from the outside in
    workingRingTiles=Layer.getTilesBorderXYSelect([waXs+ring,waYs+ring],[waXe-ring,waYe-ring])
    for tile in workingRingTiles:
        # if 0 oceantiles placed chance should be 100%, if all oceantiles placed chance should be 0%
        print("landTiles "+str(landTiles)+" oceantiles "+str(oceanTiles))
        roll = random.randint(1,max((landTiles+oceanTiles),1))
        if (roll<=oceanTiles):
            oceanTiles=oceanTiles-1
            init_layer.setTileAt(tile,3)
        else:
            init_layer.setTileAt(tile,5)
            landTiles=landTiles-1
"""





##roll = random.randint(0,99)
"""
if (roll<landPercentage):
    init_layer.setTileAt(tile,5) # 5 is land
else:
    init_layer.setTileAt(tile,3) # 3 is shallow ocean
"""









## After layer is finished add it to map
map.addLayerToMap(init_layer.getLayerData())

# TODO edit tiles in a layer straight from index 

# TODO route from a to b

# TODO layer.returnSimilarArea(startingXY) #paint bucket tool




if input("Save map file "+filename+" to "+Paths.maps()+"?\n(Input (y) To save)\n")=="y":
    map.saveMapAs(filename)


# TODO map functions to update metadata not relevant to tiled
#map.initialize(mw,mh,mtxY)
