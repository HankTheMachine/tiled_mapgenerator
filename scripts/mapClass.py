import json
import os
from .dirClass import Directory
from .layerClass import Layer
from .paths import Paths
from .tilesets import tilesets

class HexMap:
    """
    Hexagonixally oriented map. If a .tmj map file with the specified path and filename is found, the data in file is loaded to the Map object.
    """
    def __init__(self,mapName,mapData=None) -> None:
        self.dir = Directory(Paths.maps())
        self.filename = Directory.setExtension(mapName,".tmj")
        self.mapData = mapData
    
    def loadMap(self):
        """
        If a map by this exact name is found in maps folder, loads map's data to this Map object
        """
        if self.dir.fileExists(self.filename):
            print("Found a map file: "+self.filename)
            self.setData(self.dir.readfile(self.filename))
        else:
            print("No map under the name "+self.filename+" found.")

    def newEmptyMap(self,width,height,tilex,tiley):
        """
        Sets map data to a fresh map file!
        """
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
        md["tilesets"].append(tilesets["tileset_init"])
        self.setData(md)

    def getData(self):
        if self.mapData==None:
            print("Warning: map data is None in "+self.filename)
        return self.mapData
    
    def setData(self,data):
        self.mapData = data
    
    def setName(self, filename):
        self.filename = Directory.setExtension(filename,".tmj")

    def getLayers(self):
        return self.mapData["layers"]

    def findLayer(self,layername):
        try:
            for layer in self.mapData["layers"]:
                if layer["name"]==layername:
                    return Layer(layer)
            return None
        except TypeError:
            print("TypeError seeking layer "+layername+" at :"+self.filename+": No data in map object.")
            
    def setLayer(self,layerData):
        for layer in self.mapData["layers"]:
            if layer["name"]==layerData["name"]:
                layer = layerData
    
    def addLayerToMap(self,layerData):
        self.mapData["layers"].append(layerData)
            
    def saveMapAs(self,filename):
        mapJson = json.dumps(self.mapData, indent=4)
        fn = self.dir.setExtension(filename, ".tmj")
        self.dir.writeToFile(mapJson,fn)

    def mapOnFileExists(self):
        return self.dir.fileExists(self.filename)
        

