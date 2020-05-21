"""
Polycat Animations project file structure creation

python3

This is the class for acting on a polycat project folder structure.
It uses a json file to describe a "project level key" whos contents declare the folder names that are required for that level.

    -   parent levels are keys in the json data file
    -   parent paths are path lib objects to the file path that you want to act on

In the json file there are dictionaries and lists, dictionary items are designed to be used as an important project level and will always have a 
series of child paths. Dictionary lists are designed for folder names that need to be iterated over or have no child paths that are created by the 
class. To add new folders to existing levels all you need to do is add the folder name to the correct section in the json file.

There are 3 main methods to be used in the class,

    -   makeSequence : makes a sequence and adds cuts to it
    -   makeACut : makes a single cut with a custom name, used to insets cuts between shots, needs a sequence to be created first.
    -   makCuts : makes several new cuts in a sequence starting +10 rounded from the latest cut needs a sequence to be created first.
    -   makeAsset : adds in the structure for topLevel assets

"""

import pathlib
import json
import re
from math import floor

class PcProject():

    CLIENTROOT = pathlib.Path("C:/Users/Administrator/Desktop/YARN/projects")

    def __init__(self,client,job):

        self.JLEVELS = self.getJson(r"project_structure\json\constantLevels.json")
        self.projroot = self.CLIENTROOT / client
        self.jobroot = self.projroot / job
        
        #job level paths
        self.jobAaa = self.makeLevelPath(self.jobroot,"jobLevel","jobClient")
        self.jobAssets = self.makeLevelPath(self.jobroot,"jobLevel","jobAssets")
        self.jobSequences = self.makeLevelPath(self.jobroot,"jobLevel","jobSequences")
        self.jobDevelopment = self.makeLevelPath(self.jobroot,"jobLevel","jobDevelopment")
        self.jobEdit = self.makeLevelPath(self.jobroot,"jobLevel","jobEdit")
        self.jobLitterBox = self.makeLevelPath(self.jobroot,"jobLevel","jobLitterbox")

        #asset level paths
        self.assetAudio = self.makeLevelPath(self.jobAssets,"assetLevel","assetAudio")
        self.assetCharacters = self.makeLevelPath(self.jobAssets,"assetLevel","assetCharacters")
        self.assetEnvironment = self.makeLevelPath(self.jobAssets,"assetLevel","assetEnvironment")
        self.assetProp = self.makeLevelPath(self.jobAssets,"assetLevel","assetProps")
        self.assetVfx = self.makeLevelPath(self.jobAssets,"assetLevel","assetVfx")

        self.makeClient("clientLevel",self.jobAaa)
        self.makeEdit(self.jobEdit)
        self.makeLitterBox("users",self.jobLitterBox)

    def getJson(self,jpath):
        
        with open(jpath) as f:
            data = json.load(f)

        return data

    def makeLevelPath(self,parentpath,parentlevel,level):
        """
        parentpath = pathlibobject
        parentlevel = the name of the parent level you are trying to accsess from the json file
        level = the levelname (folder name) that you want from the json file
        """
        #the eval() is there to catch the syntax exeption caused by not passing a pathlib object into the parentpath argument
        try:
            levelpath = eval(r"parentpath / self.JLEVELS[parentlevel][level]")
            self.makeDirs(levelpath)
            return levelpath
        except:
            print("could not get the path, check that you have entered the correct data into makeLevelPath")
            return None
        
    def getSequence(self,seqname):
        """
        This just returns a pathlib path of new sequence, it does not make the path!. To be used in the makeCuts method
        """
        seqname = self.jobSequences / seqname

        if seqname.exists():
            return seqname
        else:
            print("The sequence does not exist, rather use makeSequece to create it")
            return False
        
    def makeSequence(self,seqname,numcuts):
        
        parentpath = self.jobSequences / seqname
        self.makeDirs(parentpath)
        self.makeCuts(parentpath,numcuts)

    def getDevelopment(self,devname):
        """
        This just returns a pathlib path of new development sequence, it does not make the path!. To be used in the makeCuts method
        """
        
        devname = self.jobDevelopment / devname
        return devname

    def makeDevelopment(self,devname,numcuts):

            parentpath = self.getDevelopment(devname)
            self.makeCuts(parentpath,numcuts)

    def makeCuts(self,parentpath,numcuts):
        """
        Makes cuts in a sequence. A sequence can be dev or seq
        
        parentpath = the sequence path that holds the cuts, usually self.getSequence() or self.getDevelopment()
        numcuts = The number of cuts to make in the sequence

        """
        cutlist = self.createCutList(parentpath)
        
        if not cutlist:
            cutlist.append(10)
        else:
            for newcut in range(numcuts):
            #The Floor just makes sure that the cut increments are rounded and that we dont catch a custom cut number
                cutlist.append((floor(cutlist[-1] / 10 ) *10)+10) 

        for cut in cutlist:
            
            increment = str(cut).zfill(4)
            cutname = "cut" + increment

            self.makeACut(parentpath,cutname)
    
    def makeACut(self,parentpath,cutname):

        if parentpath:

            cutpath = parentpath / cutname
            self.makeLevelDictItems("cutLevel",cutpath)
        
            userpath = cutpath / self.JLEVELS["cutLevel"]["cutUsers"]
            self.makeLevelListItems("users",userpath)

            for child in userpath.iterdir():
                self.makeLevelListItems("software",child)  
        
        else:
            print("The parent path does not exist,probably because you used self.getSequence as an argument Rather use self.makeSequence(seqname,numcuts) to create the sequence and cuts")
  
    def createCutList(self,parentpath):

        repattern = r"\d+"
        cutlist = []
        cutstart = int(10)

        if parentpath:           

            chilren = parentpath.iterdir()
        
            for i in chilren:
                if i.is_dir():
                    match = re.findall(repattern,i.name)
                    cutlist.append(int(match[0]))

            if cutlist:
                cutlist.sort()        
                # cutstart = cutlist[-1] + int(10)
        
        return cutlist
        
    def makeAsset(self,parentlevel,assetname):
        """
        makes an asset and user folders

        """
        assetpath = parentlevel / assetname
        self.makeLevelDictItems("cutLevel",assetpath)
        
        userpath = assetpath / self.JLEVELS["cutLevel"]["cutUsers"]
        self.makeLevelListItems("users",userpath) 

    def makeEdit(self,path):
        
        self.makeLevelDictItems("cutLevel",path)
        
        userpath = path / self.JLEVELS["cutLevel"]["cutUsers"]
        self.makeLevelListItems("users",userpath)

        for child in userpath.iterdir():
            self.makeLevelListItems("software",child)  

    def makeLitterBox(self,parentlevel,path):
        
        self.makeLevelListItems(parentlevel,path)

    def makeClient(self,parentlevel,path):

        self.makeNestedStructure(parentlevel,path)

    def makeLevelDictItems(self,parentlevel,path):
        
        for key,value in self.JLEVELS[parentlevel].items():
            newpath = self.makeLevelPath(path,parentlevel,key)
            self.makeDirs(newpath)

    def makeLevelListItems(self,parentlevel,path):
        
        for name in self.JLEVELS[parentlevel]:
            newpath = path / name
            self.makeDirs(newpath)
            
    def makeDirs(self,path):
        
        try:
            path.mkdir(parents=True,exist_ok=True)
        except:
            print("there was an error making {0} directory".format(path))        

    def makeNestedStructure(self,parentlevelStart,path):
        
        self.makeLevelDictItems(parentlevelStart,path)

        for child in path.iterdir():
            foldername = child.name
            childpath = path / foldername
            
            self.makeLevelListItems(foldername,childpath)


## The base commands
# uvw = PcProject("uvw","xyz")
# uvw.makeSequence("scn0010_library_interior",1)
# uvw.makeCuts(uvw.getSequence("scn0010_library_interior"),1)
# uvw.makeACut(uvw.getSequence("scn0010_library_interior"),"cut0025")
# uvw.makeAsset(uvw.assetCharacters,"emprtyasset")

#TODO:
"""

"""


#ROADMAP
"""
Initial setup if a working project creation class,

get the class working in a python shell

Find a way to promote job variables to the working environment to auto set certain paths

Making a web based local host GUI that can be deployed so that people with login rights can more easily use the class


"""
