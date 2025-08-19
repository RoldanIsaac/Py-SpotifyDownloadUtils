import eyed3
from eyed3.plugins import Plugin as plugin
from eyed3.utils import guessMimetype

def getAudioTag(audiofile):
    audioTag = [
        audiofile.tag.artist,
        audiofile.tag.album,
        audiofile.tag.title,
        audiofile.tag.track_num,
        # # audiofile.tag.genre,
        # audiofile.date
        # audiofile.display
    ]
    return audioTag

def loadAudio(path):
    audiofile = eyed3.load(path)
    return audiofile

# Function in which given a file and field
# return the tag field
    # 0 Artist
    # 1 Album
    # 2 Title
    # 3 Track Number
def getTagField(file, field):
    tag = getAudioTag(loadAudio(file))
    return tag[field]

# Function in which given a list of files
# return all the artist among those files
def getManyFilesTagField(files, tag):
    fieldList = []
    for file in files:
        field = getTagField(file, tag)
        if field not in fieldList: 
            fieldList.append(field)
    return fieldList


# def setAudioTag(audiofile):
#     print("Do it")

# def getAudioFrames(audiofile):
#     for frame in audiofile.tag:
#         print(frame)


# audiofile = loadAudio("C:/Users/user/Desktop/mp3/spotifydown.com - Delphinium Blue.mp3")
# tags = getAudioTag(audiofile)
# print(tags)

# # getAudioFrames(audiofile)

# class EchoPlugin(eyed3.plugins.Plugin):
#     NAMES = ["echo"]
#     SUMMARY = u"Displays each filename and mime-type passed to the plugin"

#     def handleFile(self, f):
#         print("%s\t[ %s ]" % (f, guessMimetype(f)))