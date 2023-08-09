txtfile = open("./DEFAULT_VALUES.txt").read()
txtfilerows = txtfile.split("\n")
defaults = []

for row in txtfilerows:
    defaultvalue=row.split(" = ")[1]
    defaults.append(defaultvalue)

mapName = defaults[0]
mapx = int(defaults[1])
mapy = int(defaults[2])
tilex = int(defaults[3])
tiley = int(defaults[4])

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
    def getDefaultValues():
        return mapName,mapx,mapy,tilex,tiley