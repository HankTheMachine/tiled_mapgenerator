import json
from .defaults import Defaults


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
        self.data["data"][self.tileIndexFromXY(xy)] = tiletype

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

    def getTilesXYInRadius(self,xy,radius):
        foundtiles = []

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
            print("step e")
            xmod=1
            ymod=0
        if direct==4: #W
            print("step w")
            xmod=-1
            ymod = 0

        if direct==0: #NE
            print("step ne")
            xmod = yRemainderEast
            ymod = -1
        if direct==2: #SE
            print("step se")
            xmod = yRemainderEast
            ymod = 1
        if direct==3: #SW
            print("step sw")
            xmod = yRemainderWest*-1
            ymod = 1
        if direct==5: #NW
            print("step nw")
            xmod = yRemainderWest*-1
            ymod = -1

        if steps>1:
            return Layer.stepsToDirection([x+xmod,y+ymod],direct,steps-1)
        else: 
            return [x+xmod,y+ymod]
 
## end of class
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


