import json
import os
from .dirClass import Directory
from .layerClass import Layer
from .paths import Paths
from .defaults import Defaults

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
                layer = layerData
    

    def saveMapAs(self,filename):
        mapJson = json.dumps(self.mapData, indent=4)
        fn = self.dir.setExtension(filename, ".tmj")
        self.dir.writeJsonToFile(mapJson,fn)
        if self.prints==True:
            print("Map succesfully saved to "+self.dir.getPath()+fn+"!\n")

    def mapOnFileExists(self):
        return self.dir.fileExists(self.filename)
        

