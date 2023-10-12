import json
import os
import shutil

dir = ".\\maps\\"

def createnew(name,amount):
    """Creates a new map and assigns it a number to allow generating many. 
    """
    for x in range(amount):
        createnewNumbered(name,1)
    
def createnewNumbered(name,number):
    try:
        return open(dir+name+"-"+str(number)+".tmj", "x")
    except FileExistsError:
        return createnewNumbered(name,number+1)
    
def readfile(filename):
    if not filename[-5:] == ".tmj":
        filename=filename+".tmj"
    try:
        return json.loads(open(dir+filename).read())
    except FileNotFoundError:
        print("FileNotFoundError: "+filename+" not found at "+dir+"!")

def getMapJSON(filename):
    file = readfile(filename)
    return json.loads(file)

def getLayers(map):
    return map["layers"]