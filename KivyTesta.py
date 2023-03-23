from pickle import FALSE
from telnetlib import SE
from tokenize import String
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.label import Label
from datetime import datetime
import time
from functools import partial
import pandas as pd
import json
import os
import numpy as np
import pprint as pp
import platform as plat

kivy.require('2.0.0') # replace with your current kivy version !

#Change to true for deployment to touchscreen
Window.fullscreen = False

#User Class
class User:
    checkins = []
    def __init__(self):
        self.first_name = ""
        self.access_level = 0
        self.birthday_day = 0
        self.birthday_month = 0
        self.birthday_year = 0
        self.gender = 0
        self.total_checkins = 0
        self.total_attended_days = 0
        self.total_attended_days_consecutive = 0
        self.total_attended_weeks_consecutive = 0
        self.total_attended_hours = 0
        self.total_attended_minutes = 0
        self.image = "blank.png"
    #Getters/Setters
    #region 
    def Set_Access_Level(self, value):
        if (value >= 0) and (value < 5):
            self.access_level = value
    def Get_Access_Level(self):
        return self.access_level
    def Set_Birthday_Day(self,value):
        if (value > 0) and (value < 32):
            self.birthday_day = value
    def Get_Birthday_Day(self):
        return self.birthday_day
    def Set_Birthday_Month(self, value):
        if (value > 0) and (value < 13):
            self.birthday_month = value
    def Get_Birthday_Month(self):
        return self.birthday_month
    def Set_Birthday_Year(self,value):
        if (value > 1900) and (value < 3000):
            self.birthday_year = value
    def Get_Birthday_Year(self):
        return self.birthday_year
    def Set_Gender(self, value):
        self.gender = value
    def Get_Gender(self):
        return self.gender
    def Set_Total_Checkins(self, value):
        if (value >= 0):
            self.total_checkins = value
    def Get_Total_Checkins(self):
        return self.total_checkins
    def Set_Total_Attended_Days(self, value):
        if (value >= 0):
            self.total_attended_days = value
    def Get_Total_Attended_Days(self):
        return self.total_attended_days
    def Set_Total_Attended_Days_Consecutive(self, value):
        if (value >= 0):
            self.total_attended_days_consecutive = value
    def Get_Total_Attended_Days_Consecutive(self):
        return self.total_attended_days_consecutive    
    def Set_Total_Attended_Weeks_Consecutive(self, value):
        if (value >= 0):
            self.total_attended_weeks_consecutive = value
    def Get_Total_Attended_Weeks_Consecutive(self):
        return self.total_attended_weeks_consecutive
    def Set_Total_Attended_Hours(self, value):
        if (value >= 0):
            self.total_attended_hours = value
    def Get_Total_Attended_Hours(self):
        return self.total_attended_hours
    def Set_Total_Attended_Minutes(self, value):
        if (value >= 0):
            self.total_attended_minutes = value
    def Get_Total_Attended_Minutes(self):
        return self.total_attended_minutes
    #endregion
    #Loaders
    #region
    def LoadCheckins():
        pass
    def SaveCheckins():
        path = ''
        pass
    #endregion

#This class defines the behavior of the check in screen
class CheckinScreen(Screen):
    checkinScreenPictureBox = ObjectProperty(None)
    def checkIn(self):
        self.checkinScreenPictureBox = Image("testa.png")

#This class defines the behavior of the splash screen
class FirstSplashScreen(Screen):
    splashScreenPictureBox = ObjectProperty(None)

#This class defines the behavior of the Screen Manager
class WindowManager(ScreenManager):
    def SwapBetweenWindows(self):
        self.current = 'checkin'

#This class defines the behavior of the main(root) screen
class MainWindow(Screen):
    flag1 = 0
    def btn(self):
        if(self.flag1 == 0):
            ani = Animation(opacity=0,duration=0.25)
            ani.start(self.pictureBox)
            self.flag1 = 1
        else:
            ani = Animation(opacity=1,duration=0.25)
            ani.start(self.pictureBox)
            self.flag1 = 0

def HIDCardSwipe(self, *largs):
    sm.SwapBetweenWindows()
    #sm.current = "checkin"
    
sm = WindowManager()

class MyApp(App):
    #START Application Variables
    users = []     #create a list to hold users
    sounds = []    #create a list to hold loaded sounds
    soundList = [] #create an empty list to hold the sound list
    soundTime = 0  #Variable for tracking song length, initialized to 0.
    playingSound = 0
    debugCounter = 0
    debugTimer = 0
    #END   Application Variables
    def LoadSound(self):
        #region
        noFile = False #Set noFile to false, if we can not load the file we will set this to true
        print (plat.platform())
        if plat.platform()[0] == "L" or plat.platform()[0] == "l":
            path = "/Audio/"
        elif plat.platform()[0] == "W" or plat.platform()[0] == "w":
            path = "Audio\\" #Folder in the root directory that holds all our audio files
        dir_list = os.listdir(path) #Use the OS library to scan the directory for all files and store them in dir_list
        try: #Use exception handling in case the file does not exist
            loadFile = pd.read_json('DataBases/audioFiles.json') #Try to load audioFiles.json
        except: #If no file exists, we set noFile to true and will create one with the scanned directory.  This should only happen once on first run.
            noFile = True
                                #A file already exists, so we need to load in any new files to the end of the list
        if (noFile == False):   #if we loaded them in the dir_list order it would change a user's selected file
            fallThrough = False
            newlist = loadFile.values.tolist()    #load previous file names
            for g in newlist:
                g = str(g)            #g starts as a list, we need to convert it to a string
                g = g.replace('[','') #Byproducts of converting from JSONs to Dataframes are brackets and pops ( [ ] and ' ')
                g = g.replace(']','') #We can use the built in replace function to remove them
                g = g.replace("'",'') #Will potentially revist as there's probably a better way to do this
                self.soundList.append(g)
            for f in dir_list:
                flagged = False
                for g in newlist:
                    g = str(g) #g starts as a list, we need to convert it to a string
                    g = g.replace('[','') #Byproducts of converting from JSONs to Dataframes are brackets and pops ( [ ] and ' ')
                    g = g.replace(']','') #We can use the built in replace function to remove them
                    g = g.replace("'",'') #Will potentially revist as there's probably a better way to do this
                    if ((f == g) and (flagged == False)): #If the files in the scanned dir_list match the old list, flag and skip
                        fallThrough = False 
                        flagged = True
                    else:
                        fallThrough = True #If they don't match, fallthrough so we add it to the list
                if ((fallThrough) and (flagged == False)): #Add new sound to list if fallThrough == True and Flagged(As a match) == False
                    self.soundList.append(f)   
            dataFrame = pd.DataFrame(self.soundList)       #Convert the list into a dataframe
            dataFrame.to_json('DataBases/audioFiles.json') #Convert the dataframe to a persistant JSON
        else:
            for f in dir_list: #No file exists, so just dump the scanned directory files into a list, should happen 1x
                print(f)
                self.soundList.append(f)
            dataFrame = pd.DataFrame(self.soundList)        #Convert the list into a dataframe
            dataFrame.to_json('DataBases/audioFiles.json')  #Convert the dataframe to a persistant JSON
        print("Loading Files in:'", path, "':")
        for f in self.soundList:                                  #Load the files in the soundList and print when they load
            self.sounds.append(SoundLoader.load(path + f))
            print('Loaded: ' + f)
        #endregion

    def PlaySound(self, selector):
        t = round(time.time() * 1000)
        #    If self.sounds[selector] exists, AND The length of the playing sound is less than the current time sound has been playing, then play the new sound
        if ((self.sounds[selector]) and ((self.sounds[self.playingSound].length * 1000) < t - self.soundTime)): 
            self.sounds[selector].play() #Plays the selected sound
            self.playingSound = selector #Save the current selected song as our playing sound, since we made it in here, and the sound is playing
            self.soundTime = round(time.time() * 1000) #get the time, round it, and multiply it by 1000 to convert to milliseconds

    def LoadUsers():
        pass

    def ChuckDebugger(self):
        if (self.debugCounter % 80 == 0):
            print("Chuck: " + str(self.debugCounter) + "    Time per 80 frames: " + str(time.time() - self.debugTimer))
            self.debugTimer = time.time()
        self.debugCounter = self.debugCounter + 1

    def MainLoop(self, *largs):
        self.ChuckDebugger()
        self.PlaySound(1)
        pass

    def build(self):
        self.LoadSound() #Load all the sound files now, so they play smoothly later
        sm.add_widget(FirstSplashScreen(name='firstsplash'))
        sm.add_widget(MainWindow(name='main'))
        sm.add_widget(CheckinScreen(name='checkin'))
        sm.current = 'firstsplash'
        Clock.schedule_interval(partial(self.MainLoop, self, 2),0.00018)
        Clock.schedule_once(partial(HIDCardSwipe,self),2)
        return sm

if __name__ == '__main__':
    MyApp().run()