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
import datetime
from functools import partial
import pandas as pd
import os
import numpy as np
import platform as plat
#import playsound as ps
import threading
import serial
from cryptography.fernet import Fernet
import random

kivy.require('2.0.0') # replace with your current kivy version !
FULL_SCREEN = 0
#Change to true for deployment to touchscreen
if (plat.platform()[0] == "L" or plat.platform()[0] == "l") and FULL_SCREEN == 1:
    Window.fullscreen = True
elif (plat.platform()[0] == "W" or plat.platform()[0] == "w"):
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
    def LoadCheckins():
        pass
    def SaveCheckins():
        path = ''
        pass

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

class Monolith(App):
    #START Application Variables
    users = []     #create a list to hold users
    sounds = []    #create a list to hold loaded sounds
    soundList = [] #create an empty list to hold the sound list
    soundTime = 0  #Variable for tracking song length, initialized to 0.
    playingSound = 0
    debugCounter = 0
    debugTimer = 0
    scannedTag = 0
    scanLock = 0
    users_df = pd.DataFrame(columns=['ID', 'CIT', 'COT'])
    user_settings_df = pd.DataFrame(columns=['Name', 'ID', 'S', 'P', 'C'])

    #END   Application Variables

    if plat.platform()[0] == "L" or plat.platform()[0] == "l":
        print('Opening serial port...')
        ser = serial.Serial('/dev/ttyACM0', 500000)

    if plat.platform()[0] == "W" or plat.platform()[0] == "w":
        print('Opening serial port...')
        #ser = serial.Serial('COM8', 500000)

    def add_user_settings(self, name, ident, s, p, c):
        self.user_settings_df = self.user_settings_df.append({'Name': name, 'ID': ident, 'S': s, 'P': p, 'C': c}, ignore_index=True)

    def add_predefined_users(self):
        self.add_user_settings('Coach Jay',     '16819214', 1,'Jay.png'    ,'Orange')
        self.add_user_settings('Jackson',       '16878869',-1,'Default.png','Green')
        self.add_user_settings('Liam',          '16878885',-1,'Default.png','Green')
        self.add_user_settings('Luke',          '16878745',-1,'Default.png','Green')
        self.add_user_settings('Ibrahim',       '16878733',-1,'Default.png','Green')
        self.add_user_settings('Ryan',          '16878705',-1,'Default.png','Green')
        self.add_user_settings('Rebagrace',     '16878861',-1,'Default.png','Green')
        self.add_user_settings('Coach Larry',   '16819201',-1,'Default.png','Green')
        self.add_user_settings('Coach Harrison','16818556',-1,'Default.png','Green')
        self.add_user_settings('Coach Tim',     '16818556',-1,'Default.png','Green')
        self.add_user_settings('Cole',          '16878693',-1,'Default.png','Green')
        #self.add_user_settings('','',-1,'Default.png','Green')


    def encrypt_dataframe(df, key):
        #Encrypts a pandas DataFrame using the Fernet encryption library.
        # Convert the DataFrame to bytes
        data = df.to_csv(index=False).encode()
        # Create a Fernet object with the key
        f = Fernet(key)
        # Encrypt the data
        encrypted_data = f.encrypt(data)
        return encrypted_data

    def decrypt_dataframe(encrypted_data, key):
        #Decrypts a pandas DataFrame using the Fernet encryption library.
        # Create a Fernet object with the key
        f = Fernet(key)
        # Decrypt the data
        decrypted_data = f.decrypt(encrypted_data)
        # Convert the decrypted data to a DataFrame
        df = pd.read_csv(pd.compat.StringIO(decrypted_data.decode()))
        return df

    def LoadSound(self):
        #region
        #
        noFile = False #Set noFile to false, if we can not load the file we will set this to true
        dir_list = 0
        path = "Audio\\" #Folder in the root directory that holds all our audio files
        if plat.platform()[0] == "L" or plat.platform()[0] == "l":
            dir_list = os.listdir("Audio") #Use the OS library to scan the directory for all files and store them in dir_list
        elif plat.platform()[0] == "W" or plat.platform()[0] == "w":
            dir_list = os.listdir(path) #Use the OS library to scan the directory for all files and store them in dir_list
        try: #Use exception handling in case the file does not exist
            loadFile = pd.read_json('DataBases/audioFiles.json') #Try to load audioFiles.json
        except: #If no file exists, we set noFile to true and will create one with the scanned directory.  This should only happen once on first run.
            noFile = True
                                #A file already exists, so we need to load in any new files to the end of the list
        if (noFile == False):   #if we loaded them in the dir_list order it would change a user's selected file
            fallThrough = False
            newlist = []
            for g in range(len(loadFile)):
                newlist.append(loadFile[0][g])
            for g in range(len(newlist)):
                listItem = newlist[g]
                listItem = str(listItem)            #g starts as a list, we need to convert it to a string
                listItem = listItem.replace('[','') #Byproducts of converting from JSONs to Dataframes are brackets and pops ( [ ] and ' ')
                listItem = listItem.replace(']','') #We can use the built in replace function to remove them
                listItem = listItem.replace("'",'') #Will potentially revist as there's probably a better way to do this
                self.soundList.append(listItem)
            for f in range(len(dir_list)):
                flagged = False
                for g in range(len(newlist)):
                    listItem = newlist[g]
                    listItem = str(listItem)            #g starts as a list, we need to convert it to a string
                    listItem = listItem.replace('[','') #Byproducts of converting from JSONs to Dataframes are brackets and pops ( [ ] and ' ')
                    listItem = listItem.replace(']','') #We can use the built in replace function to remove them
                    listItem = listItem.replace("'",'') #Will potentially revist as there's probably a better way to do this
                    if ((dir_list[f] == listItem) and (flagged == False)): #If the files in the scanned dir_list match the old list, flag and skip
                        fallThrough = False
                        flagged = True
                        break
                    else:
                        fallThrough = True #If they don't match, fallthrough so we add it to the list
                if ((fallThrough) and (flagged == False)): #Add new sound to list if fallThrough == True and Flagged(As a match) == False
                    self.soundList.append(dir_list[f])
            #print(self.soundList)
            dataFrame = pd.DataFrame(self.soundList)       #Convert the list into a dataframe
            dataFrame.to_json('DataBases/audioFiles.json') #Convert the dataframe to a persistant JSON
        else:
            for f in dir_list: #No file exists, so just dump the scanned directory files into a list, should happen 1x
                print(f)
                self.soundList.append(f)
            dataFrame = pd.DataFrame(self.soundList)        #Convert the list into a dataframe
            dataFrame.to_json('DataBases/audioFiles.json')  #Convert the dataframe to a persistant JSON
        print("Loading Files in:'", path, "':")
        if plat.platform()[0] == "L" or plat.platform()[0] == "l":
            for f in self.soundList:                                  #Load the files in the soundList and print when they load(Linux)
                self.sounds.append(SoundLoader.load("Audio/" + f))
                print('Loaded: ' + f)
        else:
            for f in range(len(self.soundList)):                                  #Load the files in the soundList and print when they load
                self.sounds.append(SoundLoader.load(path + self.soundList[f]))
                print('Loaded: ' + path + self.soundList[f])
        self.PlaySound(7)
        #endregion

    def UnlockScan(self, *largs):
        self.scanLock = 0

    def PlaySound(self, selector):
        #region
        t = round(time.time() * 1000)
        #    If self.sounds[selector] exists, AND The length of the playing sound is less than the current time sound has been playing, then play the new sound
        #print (self.sounds)
        if ((self.sounds[selector]) and ((self.sounds[self.playingSound].length * 1000) < t - self.soundTime)): 
            self.sounds[selector].play() #Plays the selected sound
        #ps.playsound("Audio//" + self.soundList[selector], False)
        self.playingSound = selector #Save the current selected song as our playing sound, since we made it in here, and the sound is playing
        self.scanLock = 1
        Clock.schedule_once(partial(self.UnlockScan,self), self.sounds[self.playingSound].length)
        self.soundTime = round(time.time() * 1000) #get the time, round it, and multiply it by 1000 to convert to milliseconds
        #endregion

    def LoadUsers():
        pass

    def ReadSerial(self, *largs):
        if self.ser.isOpen():
            try:
                if (self.ser.inWaiting() > 0):
                    data_str = self.ser.read(self.ser.inWaiting()).decode('ascii')
                    print("______________________________________")
                    print("Data:")
                    print(int(data_str, 2))
                    print("______________________________________")
                    return data_str
            except UnicodeDecodeError as e:
                print(e)
                return "0"

    def MainLoop(self, *largs):
        if (self.ser.inWaiting() > 10):
            time.sleep(0.1)
            if (self.scanLock == 0):
                data = self.ReadSerial()
                data = int(data, 2)
                print('Printing User_Settings_DF: ')
                print(self.user_settings_df)
                for i in range(len(self.user_settings_df)):
                    if(data == str(self.user_settings_df.loc[i,'ID'])):
                        self.CheckInScreen(self.user_settings_df.loc[i,'Name'], "Images/" + self.user_settings_df.loc[i,'P'], self.user_settings_df.loc[i,'S'], self.user_settings_df.loc[i,'C'])
                        self.ser.write(b'3')
                        Clock.schedule_once(partial(self.SplashScreen,self), 10)
                        self.scanLock = 1
                        print(self.user_settings_df)
            else:
                self.ser.write(b'4')
                self.PlaySound(57)
                self.ser.flush()


    def SplashScreen(self, *largs):
        self.ser.flush()
        self.label1.pos = (-1000,0)
        self.label2.pos = (-1000,0)
        self.img.pos = (0,0)
        if plat.platform()[0] == "L" or plat.platform()[0] == "l":
            self.img.source = 'Images/FIRSTNewton2Logo.png'
        elif plat.platform()[0] == "W" or plat.platform()[0] == "w":
            self.img.source = 'Images\\FIRSTNewton2Logo.png'

    def CheckInScreen(self, name, imageFilePath, soundNum, color):
        if (soundNum > -1):
            self.PlaySound(soundNum)
        else:
            self.PlaySound(random.randint(58,69))
        print('Playing: ' + str(self.soundList[soundNum]))
        self.label1.text = name + ' checked in'
        self.label1.pos = (200, 150)
        self.label1.font_size = 25
        self.label1.width = 400
        self.label1.halign = 'center'
        if (name == 'Jay'):
            self.label1.font_name = 'Aurebesh.ttf'
            self.label2.font_name = 'Aurebesh.ttf'
        else:
            self.label1.font_name = 'LiberationSans-Regular.ttf'
            self.label2.font_name = 'LiberationSans-Regular.ttf'

        self.label1.text_size = (self.label1.width, None)
        self.label2.text = "Time: \n\n" + datetime.datetime.now().strftime("%I:%M %p\n %B %d, %Y")
        self.label2.pos = (200,-50)
        self.label2.halign = 'center'

        self.label2.font_size = 25
        self.img.pos = (-200,0)
        self.img.source = imageFilePath

    def BuildElements(self):
        #region
        self.window = FloatLayout()
        self.img = Image(source="Images\\FIRSTNewton2Logo.png", pos=(0,0))
        if plat.platform()[0] == "L" or plat.platform()[0] == "l":
            self.img.source = 'Images/FIRSTNewton2Logo.png'
        elif plat.platform()[0] == "W" or plat.platform()[0] == "w":
            self.img.source = 'Images\\FIRSTNewton2Logo.png'        
        self.label1 = Label(text="")
        self.label1.pos = (-1000, 0)
        self.label1.font_size = 25
        self.label1.width = 400
        self.label1.halign = 'center'
        self.label1.font_name = 'LiberationSans-Regular.ttf'
        self.label1.text_size = (self.label1.width, None)
        self.label2 = Label(text="")
        self.label2.pos = (-1000,150)
        self.label2.font_size = 25
        self.label3 = Label(text="")
        self.xcount = 0
        self.window.add_widget(self.img)
        self.window.add_widget(self.label1)
        self.window.add_widget(self.label2)
        #endregion

    def build(self):
        self.LoadSound() #Load all the sound file names into a list, in a specific order for posterity.        
        self.BuildElements()
        self.add_predefined_users()
        #self.window.add_widget(FirstSplashScreen(name='firstsplash'))
        if plat.platform()[0] == "L" or plat.platform()[0] == "l":
            Clock.schedule_interval(partial(self.MainLoop, self, 0),0.01)
        #Clock.schedule_once(partial(self.CheckInScreen,self), 9)
        return self.window

if __name__ == '__main__':
    Monolith().run()