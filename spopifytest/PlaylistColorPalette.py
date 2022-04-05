import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import csv
import cred

import seaborn as sns
from PIL import Image, ImageDraw


clientCredentialsManager = SpotifyClientCredentials(client_id=cred.client_id, client_secret=cred.client_secret)

sp = spotipy.Spotify(client_credentials_manager = clientCredentialsManager)

def playlistToCSV(creator, playlistId):

    header = ["Artist","Album", "TrackName", "TrackId","Danceability","Energy","Key","Loudness","Mode", "Speechiness","Acousticness", "Instrumentalness","Liveness","Valence","Tempo","Type", "ID", "URI", "Track-Href", "Analysis-Url", "Duration_ms","Time_signature"]

    f = open("playlistdata.csv", 'w', encoding='UTF8', newline='')

    writer = csv.writer(f)

    writer.writerow(header)

    playlist = sp.user_playlist_tracks(creator, playlistId)["items"]
    
    rowData = []

    for track in playlist:

        #Get metadata
        rowData.append(track["track"]["album"]["artists"][0]["name"])
        rowData.append(track["track"]["album"]["name"])
        rowData.append(track["track"]["name"])
        rowData.append(track["track"]["id"])

        #Get audio features
        audioFeatures = sp.audio_features((track["track"]["id"]))[0]
        for feature in audioFeatures:
            rowData.append(audioFeatures[feature])

        writer.writerow(rowData)
        rowData.clear()

    f.close()

class Track:
    def __init__(self, title):
        self.title = title
        self.red = 0
        self.green = 0
        self.blue = 0
        

    def setRed(self, energy):
        self.red = int(energy * 255)

    def modifyRed(self, percent):
        self.red = int(self.red * percent)

    def setGreen(self, dance):
        self.green = int(dance * 255)

    def modifyGreen(self, percent):
        self.green = int(self.green * percent)

    def setBlue(self, valence):
        self.blue = int(valence * 255)

    def modifyBlue(self, percent):
        self.blue = int(self.blue * percent)

    def getRed(self):
        return self.red

    def getGreen(self):
        return self.green

    def getBlue(self):
        return self.blue

    def printData(self):
        print("\n",self.title)
        print(self.red, " ", end="")
        print(self.green, " ", end="")
        print(self.blue, " ")
        


  

class playlistColorizer:
    def __init__(self, playlistId):
        self.playlist = sp.playlist_tracks(playlistId)["items"]
        self.trackList = []
        self.colorMap = []

    def colorizeTracks(self):
        for track in self.playlist:
            newTrack = Track(track["track"]["name"])
            audioFeatures =  sp.audio_features((track["track"]["id"]))[0]

            #This is a bad way to do this lol but its 8am

            for feature in audioFeatures:
                if feature == "energy":
                    newTrack.setBlue(audioFeatures[feature])
                elif feature == "danceability":
                   newTrack.setGreen(audioFeatures[feature])
                elif feature == "valence":
                    newTrack.setRed(audioFeatures[feature]) 
                    if audioFeatures[feature] > 0.5:
                        newTrack.modifyRed(1.2)
                        newTrack.modifyGreen(1.2)
                elif feature == "mode":
                    if audioFeatures[feature] == 0:
                        newTrack.modifyRed(0.4)
                        newTrack.modifyGreen(0.4)
                        newTrack.modifyBlue(0.4)
                elif feature == "tempo":
                    if audioFeatures[feature] > 120:
                        newTrack.modifyRed(1.2)
                        newTrack.modifyBlue(1.2)
                elif feature == "loudness":
                    if audioFeatures[feature] > -6:
                        newTrack.modifyRed(1.2)
                elif feature == "acousticness":
                    if audioFeatures[feature] >= 0.1:
                        newTrack.modifyGreen(1.1)


            self.trackList.append(newTrack)

    def displayTracks(self):
         for Track in self.trackList:
             Track.printData()

    def nearestSquare(self, num):
         num1 = round(sqrt(num))**2
         return (num1)

    
    def createColorPalette(self):

        for Track in self.trackList:
            rgbCode = (Track.getRed(), Track.getGreen(), Track.getBlue())
            self.colorMap.append(rgbCode)


    def drawColorPalette(self):
       
        iter = len(self.colorMap)

        palette = self.colorMap

        width_px=1000
        new = Image.new(mode="RGB", size=(width_px,120))

        for i in range(iter):

            newt = Image.new(mode="RGB", size=(width_px//iter,100), color=palette[i])
            new.paste(newt, (i*width_px//iter,10))

        new.show()

    

pc = playlistColorizer("37i9dQZF1DXaUDcU6KDCj4")
pc.colorizeTracks()
pc.displayTracks()  

pc.createColorPalette()
pc.drawColorPalette()






#playlistToCSV("mithril.armor","7Bjxn0II09CJbNJjHp7iDj")








                


