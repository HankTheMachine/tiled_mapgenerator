import os
import json
import sys

from scripts.dirClass import Directory
from scripts.mapClass import HexMap as Map ## only hexmaps supported as of now
from scripts.layerClass import Layer
from scripts.paths import Paths
from scripts.defaults import Defaults
print("")
try:
    args=[]
    for arg in range(1,6):
        args.append(sys.argv[arg])
    filename, mapx, mapy, tilex, tiley = args
except IndexError:
    filename, mapx, mapy, tilex, tiley = Defaults.getDefaultValues()

map = Map(filename)
if map.mapOnFileExists() == True:
    map.loadMap()

if map.getData() == None:
    map.newEmptyMap(mapx, mapy, tilex, tiley)

init_layer = Layer(map.findLayer("Init"))
if init_layer.getLayerData() == None:
    init_layer.newEmpty(mapx,mapy,"Init")
    map.addLayerToMap(init_layer.getLayerData())



if input("\nSave map file "+filename+" to "+Paths.maps()+"?\n(Input (y) To save)\n")=="y":
    map.saveMapAs(filename)



##print(len(map.getLayers()))
# TODO: make map initialization use data instead of path (like layer)
#
# map = HexMap.newEmptyMap()
# TODO: python if not enough arguments alternative

# TODO create another json to hold map metadata
#map.initialize(mw,mh,mtxY)

# TODO: 
# if mapexists:
# mapDataOnFile = mapsdir.readfile(filename)
# map.setData(mapDataOnFile)
#else:
# do stuff to make a new empty map


"""
map = Map(mapsdir.getPath(),filename)
if not mapsdir.fileExists(filename):
    if len(sys.argv) >= 6:
        mh = sys.argv[2]
        mw = sys.argv[3]
        tilex = sys.argv[4]
        tiley = sys.argv[5]
    else:
        mh = int(input("Input map height in tiles: "))
        mw = int(input("Input map width in tiles: "))
        tilex = int(input("Input tile width in pixels: "))
        tiley = int(input("Input tile width in pixels: "))
    map.setData(map.newEmptyMap(mh,mw,tilex,tiley))
    initlayer = Layer.createEmpty(mh,mw,"Init")
    map.addLayerToMap(initlayer.getLayerData())
else:
    mh = map.getData()["height"]
    mw = map.getData()["width"]
    tilex = map.getData()["tileheight"]
    tiley = map.getData()["tilewidth"]

initlayer = map.findLayer("Init")

initlayer2 = Layer.createEmpty(mh,mw,"Init2")
# TODO: change layer ID upon adding to map
map.addLayerToMap(initlayer2.getLayerData())



## TODO make this better
##init_layer = Layer(smthsmth)




"""



"""
initlayer = Layer(map.findLayer("Init"))

initlayerdata = initlayer.getLayerData()
print(initlayerdata["data"])
#print( initlayer.getLayerData() )
"""
"""
testTuple = (8,3)
print(testTuple[0]) #this works
"""
# TODO route from a to b

# TODO make multiple layers for different stuff

# TODO edit tiles in a layer straight from index 

# TODO layer.returnSimilarArea(startingXY) #paint bucket tool

"""
filename = "Editor_30x30"

map=mps.getMapJSON(filename)
allLayers = mps.getLayers(map)
layer = lrs.find(allLayers,"Init")

#print(lrs.adjacentTilesXY(layer,0,0))
tile = 60
x,y = lrs.tileNrToXY(layer,tile)
print(x,y)
print(lrs.tileat(layer,x,y))

#  30 31         31 32
# 60 61 62      61 62 63 
#  90 91
"""



"""
radiustiles = Layer.getTilesXYInRadius([10,10],4)
print("Radius of tiles:")
print(radiustiles)
for tilexy in radiustiles:
    initlayer.setTileAt(tilexy,11)

initlayer.setTileAt([10,10],3)
"""

"""
initlayerdata = initlayer.getLayerData()
map.setLayer(initlayerdata)

"""









#map.showData()
##map.getPath()
##dir.listMaps()
#ap = Map(path,"Editor_30x30",dir)
"""
filedata = dir.readfile("Editor_30x30")
print(filedata)
map.
"""