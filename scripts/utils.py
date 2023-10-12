import json
import os

import math
from scripts.defaults import Defaults
from scripts.defaults import Paths
#from .tilesets import tilesetsDev as tilesets
from .tilesets import tilesets

class HexMap:
    """
    Hexagonixally oriented map. If a .tmj map file with the specified path and filename is found, the data in file is loaded to the Map object.

    If prints is set to True prints things about operations regarding to itself.
    """
    def __init__(self,mapName,mapData=None,) -> None:
        self.dir = Directory(Paths.maps())
        self.filename = Directory.setExtension(mapName,".tmj")
        self.mapData = mapData
        self.prints = Defaults.printFeedBack()
        if self.prints == True:
            print("Map: "+self.filename+"\n")
    
    def loadMap(self):
        """
        If a map by this exact name is found in maps folder, loads map's data to this Map object
        """
        fileExists = self.dir.fileExists(self.filename)
        if fileExists == True:
            self.setData(self.dir.readfile(self.filename))
            if self.prints == True:
                mapx,mapy,tilex,tiley = self.getDimensions()
                print("Found map file "+Paths.maps()+Directory.setExtension(self.filename,".tmj")+" with dimensions: "+str(mapx)+"x"+str(mapy)+" (tiles "+str(tilex)+"x"+str(tiley)+") ...\n")
        else:
            if self.prints == True:
                print("No map data found at "+Paths.maps()+Directory.setExtension(self.filename,".tmj"))

    def setprinting(self, bool):
        """
        Toggle printing in object. Input True or False. Use for debugging.
        """
        self.prints = bool

    def newEmptyMap(self,width,height,tilex,tiley):
        """
        Sets map data to a fresh map file!
        """
        if self.prints==True:
            print("Creating new map with dimensions: "+str(width)+"x"+str(height)+" (tiles "+str(tilex)+"x"+str(tiley)+") ...\n")
        md = {}
        md["compressionlevel"] = -1
        md["height"] = height
        md["hexsidelength"] = int((tilex+tiley)/4) ## works with 64x64 but is this right?
        md["infinite"]='false'
        md["layers"]= []
        md["nextlayerid"]=2
        md["nextobjectid"]=1
        md["orientation"]="hexagonal"
        md["renderorder"]="right-down"
        md["staggeraxis"]="y"
        md["tiledversion"]="1.10.1"
        md["tileheight"]=tilex
        md["tilesets"]=[]
        md["tilewidth"]=tiley
        md["type"]="map"
        md["version"]="1.10"
        md["width"]=width
        self.setData(md)

    def getData(self):
        """
        Returns ALL data saved in the Map object during script runtime
        """
        return self.mapData
    
    def setData(self,data):
        """
        Sets ALL data in Map object to input. Overwrites everything!
        """
        self.mapData = data
    
    def setName(self, filename):
        self.filename = Directory.setExtension(filename,".tmj")

    def getDimensions(self):
        mapx = self.mapData["width"]
        mapy = self.mapData["height"]
        tilex = self.mapData["tilewidth"]
        tiley = self.mapData["tileheight"]
        return mapx,mapy,tilex,tiley

    def getLayers(self):
        return self.mapData["layers"]
    
    def getLayerNames(self):
        list = self.getLayers()
        listofnames = []
        for layer in list:
            listofnames.append(layer["name"])
        return listofnames

    def getTileSets(self):
        """
        Returns all tilesets in mapData
        """
        return self.mapData["tilesets"]

    def hasTileSet(self, tilesetname):
        """
        Returns true or false depending if a tileset by specified name exists in map data
        """
        for tilest in tilesets:
            if tilest["name"]==tilesetname:
                return True
        return False    
        
    def addTileSet(self, tilesetname):  
        """
        Finds appropriate tileset from .tilesets.py and adds its data to mapData.
        """
        for tilest in tilesets:
            if tilest["name"]==tilesetname:
                if self.mapData["tilesets"].count(tilest["data"]) == 0:
                    self.mapData["tilesets"].append(tilest["data"])


    def listLayers(self, prints=None):
        """
        Returns a list of tuples in the format (layerid, layername). Default behaviour based on self.prints -> prints the list if true. Can be togggled with parameter boolean.
        """
        if prints == None:
            prints=self.prints

        lrsList=[]
        for layer in self.mapData["layers"]:
            lrTuple = tuple([layer["id"],layer["name"]])
            lrsList.append(lrTuple)
        if prints == True:
            print("Layers in map:")
            print(lrsList)
        return lrsList

    def findLayer(self,layerid,returnAsData=False):
        """
        Finds and returns a layer Object of the layer sought. Accepts as argument either id as int or name as string.
        """
        if returnAsData==False:
            if type(layerid) == str:
                for layer in self.mapData["layers"]:
                    if layer["name"]==layerid:
                        return Layer(layer["name"],layer)
                return None
            
            if type(layerid) == int:
                for layer in self.mapData["id"]:
                    if layer["id"]==layerid:
                        return Layer(layer["name"],layer)
                return None
            
        else:
            if type(layerid) == str:
                for layer in self.mapData["layers"]:
                    if layer["name"]==layerid:
                        return layer
                return None
            
            if type(layerid) == int:
                for layer in self.mapData["id"]:
                    if layer["id"]==layerid:
                        return layer
                return None
        """
        try:
            for layer in self.mapData["layers"]:
                if layer["name"]==layerid:
                    return Layer(layer)
            return None
        except TypeError:
            print("TypeError seeking layer "+layerid+" at :"+self.filename+": No data in map object.")
        """

    def deleteLayer(self,id):
        """
        Deletes from map data the first layer that matches id submitted as parameter
        """
        layers=self.mapData["layers"].copy()
        for layer in range(len(layers)):
            if layers[layer]["id"]==id:
                deletedName=layers[layer]["name"]
                del self.mapData["layers"][layer]
                if self.prints == True:
                    print("Deleted layer id "+str(id)+": "+deletedName)
                break
        
        


    def findAvailableLayerId(self):
        layerIds = []
        for layer in self.mapData["layers"]:
            layerIds.append(layer["id"])
        
        if self.prints==True:
            print("Ids present in map data:")
            print(layerIds)
        
        id = 1
        while id in layerIds:
            id = id+1
        return id

    def addLayerToMap(self,layerData):
        newId = self.findAvailableLayerId()

        layerData["id"] = newId
        if self.prints == True:
            layername = layerData["name"]
            print("Adding layer "+layername+" to map at ID n:o "+str(newId)+"...\n")
        self.mapData["layers"].append(layerData)
            
    def setLayer(self,layerData):
        for layer in self.mapData["layers"]:
            if layer["name"]==layerData["name"]:
                self.mapData["layers"].remove(layer)
                self.mapData["layers"].append(layerData)
    

    def saveMapAs(self,filename):
        mapJson = json.dumps(self.mapData, indent=4)
        fn = self.dir.setExtension(filename, ".tmj")
        self.dir.writeJsonToFile(mapJson,fn)
        if self.prints==True:
            print("Map succesfully saved to "+self.dir.getPath()+fn+"!\n")

    def mapOnFileExists(self):
        return self.dir.fileExists(self.filename)
        
class Layer:
    """
    An object representing a single layer in the map. When initializing, if no data is provided, a default empty layer is initialized.
    """
    def __init__(self,layername="New Layer",data=None,width=Defaults.mapWidth(),height=Defaults.mapHeight()):
        self.layername = layername
        self.data = data
        self.prints = Defaults.printFeedBack()
        if self.data==None:
            self.newEmpty(height,width)
        self.allowedArea = self.getTilesBoxSelect((0,0),(self.data["width"],self.data["height"]))
    
    def setprinting(self, bool):
        """
        Toggle printing in object. Input True or False. Use for debugging.
        """
        self.prints = bool

    def newEmpty(self,w,h):
       
        layerdata = {}
        layertiles = []

        if self.prints == True:
            for x in range(w*h):
                if x%3 == 0:
                    print("Creating new empty layer with the name "+self.layername+"...", end="\r")
                elif x%2 == 0:
                    print("Creating new empty layer with the name "+self.layername+"..", end="\r")
                else:
                    print("Creating new empty layer with the name "+self.layername+".", end="\r")
                layertiles.append(0)
            print("\nEmpty layer initialized successfully!\n")
        else:
            for x in range(w*h):
                layertiles.append(0)

        layerdata["data"] = layertiles
        layerdata["height"] = h
        layerdata["id"] = 1
        layerdata["name"] = self.layername
        layerdata["opacity"] = 1
        layerdata["type"] = "tilelayer"
        layerdata["visible"] = 'true'
        layerdata["width"] = w
        layerdata["x"] = 0
        layerdata["y"] = 0
        self.setData(layerdata)

    def setName(self,newname):
        self.layername = newname
        self.data["name"] = newname

    def getName(self):
        return self.layername
    
    def setData(self,data):
        """
        Sets ALL of the data associated with the layer to speficied input. Treat as a save, this overwrites everything previously saved in object.
        """
        self.data = data
  
    def getLayerData(self):
        """
        Returns the whole layer data
        """
        return self.data
    
    def setAllowedArea(self,areaStart,areaEnd):
        """
        Sets the area allowed to edit by the setTile function
        """
        self.allowedArea = self.getTilesBoxSelect(areaStart, areaEnd)
    
    def setLayerTileGrid(self,tileArray):
        """
        Sets tile array to input
        """
        self.data["data"] = tileArray

    def getLayerTileGrid(self):
        """
        Returns the array of tiles in the layer
        """
        return self.data["data"]
    
    
    def setName(self,layername):
        """
        Sets layer name to specified input
        """
        self.data["name"] = layername

    def setId(self, id):
        """
        Changes the layer id to input. Use when adding layer to map.
        """
        self.data["id"] = id

    def setOpacity(self,opacity):
        """
        Set layer opacity to input. Input float between 0 and 1.
        """
        if opacity > 1:
            opacity=1
        if opacity < 0:
            opacity=0
        self.data["opacity"] = opacity
        
    def setVisibility(self,visibility=1):
        """
        1 for visible, 0 for invisible
        """
        if not visibility == (0 or 1):
            visibility=1
        if visibility==0:
            self.data["visible"]='false'
        if visibility==1:
            self.data["visible"]='true'

    def getTilesBasedOnNeighbours(self,area,neighbors,condition):
        filteredTiles=[]
        if condition=="Any":
            for tile in area:
                for neighbor in neighbors:
                    if neighbor in self.getNeighboringTileTypes(tile):
                        filteredTiles.append(tile)
        if condition=="All":
            for tile in area:
                tilesBool=True
                for neighboringTile in self.getNeighboringTileTypes(tile):
                    if neighboringTile not in neighbors:
                        tilesBool=False
                if tilesBool==True:
                    filteredTiles.append(tile)
        

        return filteredTiles

    def filterTilesByType(self,area,types):
        tiles = []
        
        for tile in area:
            for type in types:
                if self.getTileAt(tile)==type:
                    tiles.append(tile)
        return tiles

    def tileIndexFromXY(self,xy):
        lrw = self.data["width"]
        lrh = self.data["height"]
        if (xy[0] or xy[1]) < 0 or xy[0] >= lrw or xy[1] >= lrh:
            print(str(xy[0])+", "+str(xy[1])+" is outside layer dimensions!")
            return None
        else:
            return xy[0] + int(xy[1]*lrw)
    
    def setTileAt(self,xy,tiletype):
        """
        Sets tile at location {tuple(x,y)} to {tiletype} on this layer.
        """
        x=xy[0]
        y=xy[1]
        
        if [x,y] in self.allowedArea:
            self.data["data"][self.tileIndexFromXY(xy)] = tiletype

    def getTileAt(self,xy):
        """
        Returns the tile data value in layer at point {tuple(x,y)}
        """
        x,y = xy[0],xy[1]
        if y >= self.data["height"] or x >= self.data["width"] or (x or y) < 0:
            return 0
        try:
            return self.data["data"][self.tileXYtoNr(x,y)]
        except IndexError:
            return 0

    def tileXYtoNr(self,x,y):
        no = x+(y*self.data["width"])
        return no
    
    def getRelativeLocation(self,xy,xymod):
        xnew = xy[0]+xymod[0]
        ynew = xy[1]+xymod[1]
        return [xnew,ynew]

    def createOceanBorder(self):
        mapx = self.data["width"]
        mapy = self.data["height"]
        for tile in self.getTilesBorderXYSelect([0,0],[mapx-1,mapy-1]):
            self.setTileAt(tile,1)
        for tile in Layer.getTilesBorderXYSelect([1,1],[mapx-2,mapy-2]):
            self.setTileAt(tile,2)
        for tile in Layer.getTilesBorderXYSelect([2,2],[mapx-3,mapy-3]):
            self.setTileAt(tile,3)

    def getCenterPoint(self):
        """
        Returns x and y of center point in map
        """
        x=math.floor(int(self.data["width"])/2)
        y=math.floor(int(self.data["height"])/2)
        return x,y
    
    def tileDistanceToBorder(self,xy):
        x=xy[0]
        y=xy[1]
        toBottom = self.data["height"]-y
        toRight = self.data["width"]-x
        return min(x,y,toBottom,toRight)

        

    @staticmethod
    def getTilesBoxSelect(xystart,xyend):
        """
        Returns list of xy values in a box from xystart to xyend
        """
        tilesInBox = []
        xDifference = xyend[0]-xystart[0]+1
        yDifference = xyend[1]-xystart[1]+1
        for horiz in range(xDifference):
            for vertic in range(yDifference):
                xytuple = [(xystart[0]+horiz),(xystart[1]+vertic)]
                tilesInBox.append(xytuple)
        return tilesInBox

    @staticmethod
    def getTilesBorderXYSelect(xystart,xyend):
        foundtiles = []
        xdiff = xyend[0]-xystart[0]
        ydiff = xyend[1]-xystart[1]
        for x in range(xdiff+1):
            foundtiles.append([xystart[0]+x,xystart[1]])
            foundtiles.append([xystart[0]+x,xyend[1]])
        for y in range(ydiff+1):
            foundtiles.append([xystart[0],xystart[1]+y])
            foundtiles.append([xyend[0],xystart[1]+y])
        return foundtiles

    #NE, E, SE, SW, W, NW
    #6*1,3*6,6*6
    #6(ne),6(n+2)
    #1,3,6,10

    def getNeighboringTileTypes(self,xy):
        tiles = self.getTilesXYInRadiusBorder(xy,1)
        tileTypes = []
        for tile in tiles:
            tileType = self.getTileAt(tile)
            tileTypes.append(tileType)
        #print(tileTypes)
        return tileTypes

    def getTilesByType(self,area,type):
        for tile in area:
            if self.getTileAt(tile) != type:
                area.remove(tile)
        return area

    def getTilesXYInRadius(self,xy,radius):
        foundtiles = []
        foundtiles.append(tuple(xy))
        for direction in range(6):
            for steps in range(radius):
                foundXY = xy
                foundXY = Layer.stepsToDirection(xy,direction,steps)
                #first add the tile that is steps+1 tiles away straight ahead
                foundtiles.append(tuple(foundXY))
                #now iterating from this tile onwards on :
                for i in range(steps-1):
                    #2nd iteration onwards also add the tile that is 1 tile towards the other direction
                    foundXY = Layer.stepsToDirection(foundXY,direction-2,1)
                    foundtiles.append(tuple(foundXY))
        return set(foundtiles)

    def getTilesXYInRadiusBorder(self,xy, radius):
        allTiles = self.getTilesXYInRadius(xy,radius)
        innerTiles = self.getTilesXYInRadius(xy,radius-1)
        for tile in innerTiles:
            allTiles.remove(tile)
        return allTiles

    @staticmethod
    def stepsToDirection(xy,direct,steps):
        """
        Returns the xy of a tile one step to a direction based on integer 0-5. Used for iterating for adjacent tiles in 6 directions. Order is clockwise: NE,E,SE,SW,E,NW
        """

        x,y = xy
        yRemainderEast=y%2
        yRemainderWest=(y+1)%2

        while direct<0:
            direct=direct+6

        if direct==1: # E
            #print("step e")
            xmod=1
            ymod=0
        if direct==4: #W
            #print("step w")
            xmod=-1
            ymod = 0

        if direct==0: #NE
            #print("step ne")
            xmod = yRemainderEast
            ymod = -1
        if direct==2: #SE
            #print("step se")
            xmod = yRemainderEast
            ymod = 1
        if direct==3: #SW
            #print("step sw")
            xmod = yRemainderWest*-1
            ymod = 1
        if direct==5: #NW
            #print("step nw")
            xmod = yRemainderWest*-1
            ymod = -1

        if steps>1:
            return Layer.stepsToDirection([x+xmod,y+ymod],direct,steps-1)
        else: 
            return [x+xmod,y+ymod]
 
class Directory:
    """
    Class for functions revolving around adding, reading or deleting map files in the directory passed as an init argument
    """
    def __init__(self,path) -> None:
        self.path = str(path)
    
    def getPath(self):
        """
        Returns the path the directory object represents.
        """
        return self.path
     
    def listFiles(self):
        """
        Lists all the files in directory
        """
        print(os.listdir(self.path))

    def deleteAllNamed(self,filename):
        """
        Use for deleting multiple versions of a map. Finds and deletes map and their versions if filename before the symbol "-" matches parameter.
        """
        maps=os.listdir(self.path).copy()
        for x in maps:
            if x.split("-")[0]==filename:
                os.remove(dir+x)

    def readfile(self,filename):
        """
        Returns file data as a JSON. Handles error if file not found.
        """
        try:
            return json.loads(open(self.path+filename).read())
        except FileNotFoundError:
            print("FileNotFoundError: "+filename+" not found at "+self.path+"!")

    def fileExists(self,filename):
        """
        Returns true if file exists and false if not.
        """
        try:
            x = open(self.path+filename).read()
            return True
        except FileNotFoundError:
            pass
        return False
    
    def writeJsonToFile(self,json,filename):
        """
        Saves json to the directory with the specific filename.
        """
        with open(self.path+filename, "w") as writefile:
            writefile.write(json)

    
    @staticmethod
    def setExtension(filename,ext):
            """
            Returns filename with the speficied extension. If no file extension specified, adds the desired one or changes the inputted one
            """
            fnroot = filename.split(".")[0]
            return fnroot+ext


def tileXYtoNr(layer,x,y):
    no = x+(y*layer["width"])
    return no

def tileNrToXY(layer,tile):
    lrx = layer["width"]
    x = (tile % lrx)
    y = int((tile-x)/lrx)
    return x,y
    
def tileat(layer,x,y):
    if y >= layer["height"] or x >= layer["width"] or (x or y) < 0:
        return 0
    try:
        return layer["data"][tileXYtoNr(layer,x,y)]
    except IndexError:
        return 0

##TODO
def adjacentTiles(layer,tile):
    data=layer["data"]
    row = layer["width"]
    ##TODO: this is if tile is odd nmbr
    tilenrs = [tile-row,tile-row+1,tile-1,tile+1,tile+row,tile+row+1]
    tiles=[]
    for x in tilenrs:
        try:
            tiles.append(data[x])
        except IndexError:
            tiles.append(0)
    return tiles

def adjacentTilesXY(layer,x,y):
    return adjacentTiles(layer,tileXYtoNr(layer,x,y))
