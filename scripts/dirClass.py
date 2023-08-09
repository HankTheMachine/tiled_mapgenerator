import json
import os

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

