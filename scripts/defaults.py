txtfile = open("./PATHS.txt").read()
txtfilesplit = txtfile.split("\n")
paths = []
for row in txtfilesplit:
    path=row.split(" = ")[1]
    paths.append(path)

txtfiledefs = open("./DEFAULT_VALUES.txt").read()
txtfilerowsdefs = txtfiledefs.split("\n")
defaults = []
for row in txtfilerowsdefs:
    defaultvalue=row.split(" = ")[1]
    defaults.append(defaultvalue)

class Paths:
    def __init__(self) -> None:
        pass

    @staticmethod
    def maps():
        return paths[0]
    
    @staticmethod
    def examples():
        return paths[1]
    
    @staticmethod
    def tilesets():
        return paths[2]
    
class Defaults:
    txtfile = open("./PATHS.txt").read()
txtfilesplit = txtfile.split("\n")
paths = []
for row in txtfilesplit:
    path=row.split(" = ")[1]
    paths.append(path)

txtfiledefs = open("./DEFAULT_VALUES.txt").read()
txtfilerowsdefs = txtfiledefs.split("\n")
defaults = []
for row in txtfilerowsdefs:
    defaultvalue=row.split(" = ")[1]
    defaults.append(defaultvalue)

class Paths:
    def __init__(self) -> None:
        pass

    @staticmethod
    def maps():
        return paths[0]
    
    @staticmethod
    def examples():
        return paths[1]
    
    @staticmethod
    def tilesets():
        return paths[2]
    
class Defaults:
    def __init__(self) -> None:
        pass

    @staticmethod
    def mapName():
        return str(defaults[0])
    @staticmethod
    def mapHeight():
        return int(defaults[2])
    @staticmethod
    def mapWidth():
        return int(defaults[1])
    @staticmethod
    def tileHeight():
        return int(defaults[4])
    @staticmethod
    def tileWidth():
        return int(defaults[3])
    @staticmethod
    def printFeedBack():
        return bool(int(defaults[5]))
    @staticmethod
    def overwrite():
        return bool(int(defaults[7]))
    @staticmethod
    def landPercentage():
        return int(defaults[6])
    @staticmethod
    def getDefaultValues():
        return str(defaults[0]),int(defaults[1]),int(defaults[2]),int(defaults[3]),int(defaults[4])

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