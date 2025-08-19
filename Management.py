import os
import shutil

from importlib.machinery import SourceFileLoader
# module = SourceFileLoader("loadFolder","loadFolder.py")
# loadFolder = module.load_module()

from loadFolder import Folder


# module2 = SourceFileLoader("loadFolder","D:/_xDeveloper/@mymodules/webScrp.py")
# webScrp = module2.load_module()

CHARS = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Management(object):

    def __init__(self, path, ext):
        
        self.path = path
        self.newPath = ""
        self.ext = ext
        self.operateFolder = Folder("","")
        self.storeIdemItems = []
        self.minNumberOfItemsToCreateFolder = 0
        self.tracklist = []

        self.folderList = []
        self.folderPath = []
        self.trackedFolderList = False
        self.updates = 0
        self.groupsMade = 0

        self.operations = 0

    def sanitizePath(self,path):
        path = path.replace('\\','/')
        return path
    
    # Function to get all files in a folder and its subfolders
    # param: folder to scan
    def getAllFilesInFolder(self, parentDir): 
        
        self.operateFolder = Folder(parentDir, self.ext)
        self.operateFolder.loadAllSubfolders()
        self.operateFolder.loadItemsFolderSubFolders()

        # print("Internal: loadFolder executed successfully.")

    # Function to create list of subfolders in folder
    # param: path where to load all the folders
    def listDir(self, parentDir):

        for x in os.walk(parentDir):
            getStart = x[0].rfind('\\')

            # print(x[0][(getStart + 1):])

            currentFolder = x[0][(getStart + 1):]

            if (CHARS.find(currentFolder) == -1):
                self.folderList.append(currentFolder)
                self.folderPath.append(x[0])
            
            # The root folder has been tracked?
            self.trackedFolderList = True       

    # Function to move all the files in user selected folder 
    # to destination folder
    def initMoveFiles(self, parentDir, destinationDir):
        
        # First get all files in the user's selected folder
        self.getAllFilesInFolder(parentDir)

        # Move the files
        self.moveFiles(parentDir, destinationDir, 0)

        # print("Nothing left.")
   
    #
    # 0
    def group(self, parentDir, max):

        self.getAllFilesInFolder(parentDir)
        self.minNumberOfItemsToCreateFolder = max        
        self.compareFiles()
  
    #
    # 1
    # Function to store all the files with same prefix in an array
    def compareFiles(self): 

        itemPrefix = "" 
        self.groupsMade = 0
        for currentItem in self.operateFolder.files:
            self.storeIdemItems.clear()
            itemPrefix = currentItem.split(" - ")
            for currentSubItem in self.operateFolder.files: 
                subItemprefix = currentSubItem.split(" - ")
                if (currentSubItem != currentItem and subItemprefix[0] == itemPrefix[0]):
                    self.storeIdemItems.append(currentSubItem) 
            self.storeIdemItems.append(currentItem)

    # if the array contains more than a maxim number of items, 
    # save all of them in a folder with name like prefix and 
    # remove all the prefixes from the files saved

            if int(len(self.storeIdemItems)) > (int(self.minNumberOfItemsToCreateFolder)-1):
                
                # print(storeidemItems)

                self.groupByName(itemPrefix[0])       
  
    #                
    # 2
    def groupByName(self,itemPrefix):

        # Get potential new folder name and its path
        newDir = itemPrefix
        parentDir = self.operateFolder.path
        # Create that new folder and get its path
        destinationDir = self.operateFolder.createFolder(parentDir, newDir)

        self.moveFiles(parentDir, destinationDir, 1)
        self.renameItems(destinationDir)
        self.operateFolder.update(parentDir)
    
    #
    # 3
    def moveFiles(self, parentDir, destinationDir, source):    

        files = self.operateFolder.files if source == 0 else self.storeIdemItems
        self.operations = 0 # Counter

        self.moveMultipleFiles(files, parentDir, destinationDir)
        
        if self.operations != 0:
            # ?
            self.groupsMade += 1
 
    #        
    # 4 
    # Function to rename items in the form Artist - Title
    def renameItems(self, parentDir):

        # First get all files in the user's selected folder
        self.getAllFilesInFolder(parentDir)

        for file in self.operateFolder.files:

            try:
                itemPrefix = file.split(" - ")
                itemPathName = os.path.join(parentDir, file)
                itemnewPathName = os.path.join(parentDir,itemPrefix[1])
                os.rename(itemPathName,itemnewPathName)

            except:
                continue
    

    # Function to remove substring in all files in current folder
    # param: path where to load files
    # param: substring to remove in files
    def removeSubstring(self, parentDir, substring):

        # First get all files in the user's selected folder
        self.getAllFilesInFolder(parentDir)

        self.operations = 0 # Counter
        for file in self.operateFolder.files:

            # Remove the substring
            try:
                newFileName = file.replace(substring, '')

                filePathName = os.path.join(parentDir, file)
                filenewPathName = os.path.join(parentDir, newFileName)
                os.rename(filePathName,filenewPathName)

                self.operations += 1

            # except: continue
            except: 
                print("Ups... something went wrong -> removeSubstring function")        


    # Function to move a single file to another folder
    def moveSingleFile(self, file, parentDir, destinationDir):
        try:
            # Get the full path, which is path + file name
            # and then move
            sourceDir = os.path.join(parentDir, file)
            shutil.move(sourceDir, destinationDir)
            self.operations += 1
            return 0 # success
        except Exception as err: 
            print('Error moving file: {}'.format(file))
            print(err)

    # Function to move an array of files to another folder
    def moveMultipleFiles(self, files, parentDir, destinationDir):
        for file in files:
            self.moveSingleFile(file, parentDir, destinationDir)
        

# Methods for web scraping

#webScraping
    # def webScraping(self,URL):

    #     self.tracklist = webScrp.Scrape(URL)

#numberItems
    def numberItems(self,parentDir):

        self.getAllFilesInFolder(parentDir)

        for item in self.operateFolder.files:

            for index, list in enumerate(self.tracklist):

                list = list.replace("\"",'')

                if item.lower() == list.lower() + ".mp3":

                    if index < 9:
                        newId = "0" + str( index + 1 ) + ". " + item

                    else:
                        newId = str( index + 1 ) + ". " + item
                    
                    itemPathName = os.path.join(parentDir,item)
                    itemnewPathName = os.path.join(parentDir,newId)
                    os.rename(itemPathName,itemnewPathName)       




    ## DEPRECATED
    # Function to organize music
    # Gets a param of path to get files
    def organizeItems(self, parentDir):

        self.getAllFilesInFolder(parentDir)

        tempOperateFolder = self.operateFolder

        self.operations = 0 # Counter
        for item in tempOperateFolder.files:

            try: itemPrefix = item.split(" - ")

            except: continue

            # If there is a folder with the same name as the
            # first substring, then...
            for x, folder in enumerate(self.folderList):

                if folder == itemPrefix[0]:

                    print(" Folder will be updated: " + folder)

                    #print(self.folderPath[x])

                    try:

                        srcPath = os.path.join(parentDir,item)
                        shutil.move(srcPath,self.folderPath[x])
                        print("Success. " + item + " moved.")
                        self.operations += 1
                        self.renameItems(self.folderPath[x])

                    except:
                        print("Ups... something went wrong -> organizeItems function")        
