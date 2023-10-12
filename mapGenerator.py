import os
import json
import random
import sys
import math
from scripts.utils import HexMap as Map ## only hexmaps supported as of now
from scripts.utils import Layer
from scripts.defaults import Paths
from scripts.defaults import Defaults
from scripts.recipes.createInitLandMass import createInitialLandMass

print("\nLets make maps!")
filename, mapx, mapy, tilex, tiley = Defaults.fillDefaultValues(sys.argv)
overwrite = Defaults.overwrite()
landPercentage = Defaults.landPercentage()

#Read data or overwrite
map = Map(filename)
if (overwrite == False):
    map.loadMap() ## Does nothing if a file under filename(.tmj) not found in maps folder
    if map.getData() == None:
        map.newEmptyMap(mapx, mapy, tilex, tiley)
else:
    map.newEmptyMap(mapx, mapy, tilex, tiley)
    map.addTileSet("Init")
    map.addTileSet("Demos")

## Read the existing map layers if present
demo_layer = map.findLayer("Demo")
if demo_layer == None:
    demo_layer = Layer("Demo")
    map.addLayerToMap(demo_layer.getLayerData())

init_layer = map.findLayer("Init")
if init_layer == None:
    init_layer = Layer("Init")
    map.addLayerToMap(init_layer.getLayerData())

## Do stuff w map data
init_layer.setData(createInitialLandMass(mapx,mapy,landPercentage))

## After layers are finished update their data to map
map.setLayer(init_layer.getLayerData())
map.setLayer(demo_layer.getLayerData())
## Confirm to save
if input("\nSave map file "+filename+" to "+Paths.maps()+"?\n(Input (y) To save)\n")=="y":
    map.saveMapAs(filename)


# TODO route from a to b

# TODO layer.returnSimilarArea(startingXY) #paint bucket tool

# TODO map functions to update metadata not relevant to tiled
#map.initialize(mw,mh,mtxY)
