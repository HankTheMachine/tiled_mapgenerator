txtfile = open("./PATHS.txt").read()
txtfilesplit = txtfile.split("\n")
paths = []
for row in txtfilesplit:
    path=row.split(" = ")[1]
    paths.append(path)

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
    