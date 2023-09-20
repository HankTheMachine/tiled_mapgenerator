import os
import json
import sys
from scripts.dirClass import Directory
from scripts.mapClass import HexMap as Map ## only hexmaps supported as of now
from scripts.layerClass import Layer
from scripts.paths import Paths
from scripts.defaults import Defaults


## dont push this to main

print("\nLets make maps!")

filename, mapx, mapy, tilex, tiley = Defaults.fillDefaultValues(sys.argv)

map = Map(filename)
map.loadMap() ## Does nothing if a file under filename(.tmj) not found in maps folder
if map.getData() == None:
    map.newEmptyMap(mapx, mapy, tilex, tiley)
    
## Create the init layer, if map has one load that / if not initialize new one by said name
init_layer = map.findLayer("Init")
if init_layer == None:
    init_layer = Layer("Init")
    map.addLayerToMap(init_layer.getLayerData())

##TODO tänne jäätii

## TODO layer tiles box selection

# TODO edit tiles in a layer straight from index 

# TODO route from a to b

# TODO layer.returnSimilarArea(startingXY) #paint bucket tool


if input("Save map file "+filename+" to "+Paths.maps()+"?\n(Input (y) To save)\n")=="y":
    map.saveMapAs(filename)


# TODO map functions to update metadata not relevant to tiled
#map.initialize(mw,mh,mtxY)
