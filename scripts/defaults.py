txtfile = open("./DEFAULT_VALUES.txt").read()
txtfilerows = txtfile.split("\n")
defaults = []

for row in txtfilerows:
    defaultvalue=row.split(" = ")[1]
    defaults.append(defaultvalue)

mapName = str(defaults[0])
mapx = int(defaults[1])
mapy = int(defaults[2])
tilex = int(defaults[3])
tiley = int(defaults[4])
defaultPrints = bool(int(defaults[5]))
landPercentage = int(defaults[6])
overwrite = bool(int(defaults[7]))

class Defaults:
    def __init__(self) -> None:
        pass

    @staticmethod
    def mapName():
        return mapName
    @staticmethod
    def mapHeight():
        return mapy
    @staticmethod
    def mapWidth():
        return mapx 
    @staticmethod
    def tileHeight():
        return tiley
    @staticmethod
    def tileWidth():
        return tilex
    @staticmethod
    def printFeedBack():
        return defaultPrints
    @staticmethod
    def overwrite():
        return overwrite
    @staticmethod
    def landPercentage():
        return landPercentage
    
    @staticmethod
    def getDefaultValues():
        return mapName,mapx,mapy,tilex,tiley
    
    @staticmethod
    def fillDefaultValues(argsList):
        """
        Returns filename, mapx, mapy, tilex, tiley from provided arguments. For missing arguments default values written in DEFAULT_VALUES.txt are filled in.
        """
        args=list(Defaults.getDefaultValues())
        for arg in range(1,min(len(argsList),6)):
            args[arg-1]=argsList[arg]

        filename = str(args[0])
        mapx = int(args[1])
        mapy = int(args[2])
        tilex = int(args[3])
        tiley = int(args[4])
        return filename,mapx,mapy,tilex,tiley