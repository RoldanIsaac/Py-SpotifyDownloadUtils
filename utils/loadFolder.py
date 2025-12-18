import os
from os import listdir

    # !  Problem
    #   Select a folder, and get all the .ext files in there, 
    #   and print them in console
    # ?   What this does
    #   This class methods loads all the files in a 
    #   folder with the current extension
    #   and return them as an array

    #  Will also load all subfolders and its files

    #   Constructor
    #   path: folder
    #   ext: file extension to look for


class Folder(object):

    def __init__(self, path, ext):

        self.path = path
        self.ext = ext

        # This two next properties are the same
        # but except for the full path
        self.files = []
        self.filesPath = []

        # This two next properties are the same
        # but except for the full path
        self.allFoldersList = []
        self.allFoldersListPath = []
        
        self.trackedFolderList = False

    def init(self):
        self.loadAllSubfolders()
        self.loadItemsFolderSubFolders()
        
    # Load all subfolders in the entered path
    # this includes the folder name and the folder path
    # and a variable that becomes true if the method was executed
    def loadAllSubfolders(self):
               
        for folder in os.walk(self.path):

            # index 0 prints the full path of folder
            # index 1 prints the full path of subfolders in folder
            # index 2 prints the files in folder

            # print(folder[0]) 
               
            # last ocurrence of \, be said, the folder name, not full path
            getStart = folder[0].rfind('\\')

            # this is a int with the number of chars to the last \
            # print(getStart) 

            # getStart + 1 would be the start of folder name
            # print(folder[0][(getStart + 1):])

            currentFolder = folder[0][(getStart + 1):]

            # if (CHARS.find(currentFolder) == -1):
            self.allFoldersList.append(currentFolder)
            self.allFoldersListPath.append(folder[0])
            
            self.trackedFolderList = True 

    # Load all items in the selected folder with the extension of the class
    # Also affects the length property
    def loadItemsSingleFolder(self, selectedPath):

        self.files.clear()
        self.filesPath.clear()

        try:
            for item in os.listdir(selectedPath):
                if item.endswith(self.ext):
                    self.files.append(item)
                    self.filesPath.append(os.path.join(selectedPath, item))

            self.length = len(self.files)
        
        except:
            for item in os.listdir("C:/"):
                if item.endswith(self.ext):
                    self.files.append(item)
                    self.filesPath.append(os.path.join(selectedPath, item))

            self.length = len(self.files)

    # Load all items in all subfolders of the class path
    def loadItemsFolderSubFolders(self):

        self.files.clear()

        if (self.trackedFolderList == True):
            for folderPath in self.allFoldersListPath:
                self.loadItemsSingleFolder(folderPath)
        
        else:
            print("Warning: The class method loadAllSubfolders() hasn't been executed, please run it once at least.")

    # Show info of the class
    def showInfo(self):
        print("Extension: " + self.ext)
        print("Path: " + self.path)

        sel = input("Show all items listed? y/n.")

        if (sel == "y" or sel == "Y"):
            print("Items: ")
            for files in self.files: print(files)

    # Update the current properties running all the class methods
    def update(self):
        self.clear()
        self.loadAllSubfolders()
        self.loadItemsFolderSubFolders()



    # Change the path and the extension
    def changeSettings(self, newPath, newExt):
        self.path = newPath
        self.ext = newExt
        #
        self.update()

    # Clear all arrays
    def clear(self):
        self.files.clear()
        self.filesPath.clear()
        self.allFoldersList.clear()
        self.allFoldersListPath.clear()


    # Create new folder
    def createFolder(self, parentDir, newDirName):
        parentDir = self.path
        newDirPath = os.path.join(parentDir, newDirName)
        if not(os.path.isdir(newDirPath)):
            os.mkdir(newDirPath)

        return newDirPath

        # try:
        #     os.mkdir(newDirPath)
        # except OSError as error:
        #     print(error)
    

    def renameFile(self, parentDir, file, newName):
        try:
            itemPathName = os.path.join(parentDir, file)
            itemnewPathName = os.path.join(parentDir, newName)
            os.rename(itemPathName, itemnewPathName)
            print('Renamed: ' + file + ' -> ' + newName)
        except:
            print('Error in file: ')
            print(file)

     
# test = Folder("D:\Temp Music", ".mp3")
# test.update()
# test.showInfo()