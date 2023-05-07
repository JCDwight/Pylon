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
FULL_SCREEN = 00
#Change to true for deployment to touchscreen

def CheckPlatform():
    #Checks the platform the program is running on.  Linux = 1, Windows = 2, everything else is 3
    if (plat.platform()[0] == "L" or plat.platform()[0] == "l") and FULL_SCREEN == 1:
        return 1
    elif (plat.platform()[0] == "W" or plat.platform()[0] == "w"):
        return 2
    else:
        return 3

if ((CheckPlatform() == 1) and (FULL_SCREEN == 1)):
    Window.fullscreen = True
elif (CheckPlatform() == 2):
    Window.fullscreen = False

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
    users_df = pd.DataFrame(columns=['ID', 'CIOT', 'CIOO'])
    user_settings_df = pd.DataFrame(columns=['Name', 'ID', 'S', 'P', 'C'])
    encryption_key = 0
    encrypted_data = 0

    #END   Application Variables

    if (CheckPlatform() == 1):
        print('Opening serial port...')
        ser = serial.Serial('/dev/ttyACM0', 500000)

    if (CheckPlatform() == 2):
        print('Opening serial port...')
        #ser = serial.Serial('COM8', 500000)

    def add_user_settings(self, name, ident, s, p, c):
        self.user_settings_df = self.user_settings_df.append({'Name': name, 'ID': ident, 'S': s, 'P': p, 'C': c}, ignore_index=True)

    def add_rogue_user(self):
        pass

    #Intercept Rogue Checkins - Ah ah ah!  You didn't say the magioc word!
    def RogueCheckin(self):
        pass

    def add_predefined_users(self): #Adds pre-defined users.  Will turn this into a file once I get a new user registration screen goin
        self.add_user_settings('Coach Jay',     '16819214', 1,'jay.png'         ,'Orange')
        self.add_user_settings('Chuck Testa',   '10101010', 1,'ChuckTesta.png'  ,'Orange')
        self.add_user_settings('Jackson',       '16878869',-1,'Default.png'     ,'Green')
        self.add_user_settings('Liam',          '16878885',-1,'Default.png'     ,'Blue')
        self.add_user_settings('Luke',          '16878745',-1,'Default.png'     ,'Green')
        self.add_user_settings('Ibrahim',       '16878733',-1,'Default.png'     ,'Green')
        self.add_user_settings('Ryan',          '16878705',-1,'Default.png'     ,'Green')
        self.add_user_settings('Rebagrace',     '16878861',-1,'Default.png'     ,'Green')
        self.add_user_settings('Coach Larry',   '16819201',-1,'Default.png'     ,'Green')
        self.add_user_settings('Coach Harrison','16818556',-1,'Default.png'     ,'Green')
        self.add_user_settings('Coach Tim',     '16818556',-1,'Default.png'     ,'Green')
        self.add_user_settings('Cole',          '16878693',-1,'Default.png'     ,'Green')
        self.add_user_settings('Martin',        '16858425', 6,'Chargedup.png'   ,'Cyan')
        self.add_user_settings('Coach Shelly',  '10497184',10,'shelly.png'      ,'Gold')
        self.add_user_settings('Evan',          '16878758', 2,'EvaninFTCBox.png','Red')
        self.add_user_settings('Coach Renee',   '10497178', 8,'renee.png'       ,'Yellow')
        self.add_user_settings('Aryan',         '16878794', 4,'thisthing.png'   ,'Blue')
        self.add_user_settings('Keita',         '16878838',-1,'Default.png'     ,'Green')
        self.add_user_settings('Annabelle',     '16878841',-1,'Default.png'     ,'Purple')
        self.add_user_settings('Austin',        '16878724',-1,'Default.png'     ,'Gold')
        self.add_user_settings('Ted',           '16878757',20,'Default.png'     ,'Green')
        self.add_user_settings('Coach Craig',   '16818550', 0,'Default.png'     ,'Green')
        self.add_user_settings('Susan',         '16858448',-1,'Default.png'     ,'Green')
        self.add_user_settings('Ty',            '10518941',75,'Tytaco.png'      ,'Orange')    
        self.add_user_settings('Emma',          '16858354',-1,'Default.png'     ,'Green')
        self.add_user_settings('Vikas',         '16878849',-1,'Default.png'     ,'Green')
        self.add_user_settings('Coach Joe',     '10604432',-1,'Default.png'     ,'Purple')
        self.add_user_settings('Megan',         '16878711',-1,'Default.png'     ,'Purple')
        self.add_user_settings('Chris',         '16878807',-1,'Default.png'     ,'Purple')
        self.add_user_settings('Coach Robert',  '10497089',-1,'Default.png'     ,'Blue')
        self.add_user_settings('Coach Charles', '50444699',-1,'Default.png'     ,'Cyan')

    def LoadSound(self):
        #region
        #
        noFile = False #Set noFile to false, if we can not load the file we will set this to true
        dir_list = 0
        path = "Audio\\" #Folder in the root directory that holds all our audio files
        if (CheckPlatform() == 1):
            print("Got to check 1")
            dir_list = os.listdir("Audio") #Use the OS library to scan the directory for all files and store them in dir_list
        elif (CheckPlatform() == 2):
            print("Got to check 2")
            dir_list = os.listdir(path) #Use the OS library to scan the directory for all files and store them in dir_list
        print(dir_list)
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
        if (CheckPlatform() == 1):
            for f in self.soundList:                                  #Load the files in the soundList and print when they load(Linux)
                self.sounds.append(SoundLoader.load("Audio/" + f))
                print('Loaded: ' + f)
        else:
            for f in range(len(self.soundList)):                                  #Load the files in the soundList and print when they load
                self.sounds.append(SoundLoader.load(path + self.soundList[f]))
                print('Loaded: ' + path + self.soundList[f])
        if (FULL_SCREEN == 1):
            self.PlaySound(7)
        #endregion

    def UnlockScan(self, *largs):
        print("Unlocked scan")
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
        print("Length of song: " + str(self.sounds[self.playingSound].length))
        Clock.schedule_once(partial(self.SplashScreen,self), self.sounds[self.playingSound].length + 1)
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

    def SplashScreen(self, *largs):
        self.label1.pos = (-1000,0)
        self.label2.pos = (-1000,0)
        self.img.pos = (0,0)
        self.scanLock = 0
        print("Unlocked scan")
        if (CheckPlatform() == 1):
            self.ser.flush()
            self.img.source = 'Images/FIRSTNewton2Logo-Instructions.png'
        elif (CheckPlatform() == 1):
            self.img.source = 'Images\\FIRSTNewton2Logo-Instructions.png'

    def Simulate_Checkinorout(self,ID):
        pass

    def CheckInScreen(self, name, imageFilePath, soundNum, color, ID):
        if (CheckPlatform() == 1):
            self.ser.write(b'3')
        time.sleep(1)
        if (CheckPlatform() == 1):
            self.ser.flush()
        print("got before add")
        inorout = self.Add_Checkinorout(ID)
        if (soundNum > -1 and inorout == 1):
            self.PlaySound(soundNum)
        elif(soundNum < 0 and inorout == 1):
            self.PlaySound(random.randint(58,69))
        if (inorout == 1):
            self.label1.text = name + ' checked in!'
        else:
            self.label1.text = name + ' checked out!'

        print('Playing: ' + str(self.soundList[soundNum]))
        self.label1.pos = (200, 150)
        self.label1.font_size = 25
        self.label1.width = 400
        self.label1.halign = 'center'
        if (name == 'Coach Jay'):
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
        imageFilePath = "Images/" + imageFilePath
        self.img.source = imageFilePath

    def BuildElements(self):
        #region
        self.window = FloatLayout()
        self.img = Image(source="Images\\FIRSTNewton2Logo-Instructions.png", pos=(0,0))
        if (CheckPlatform() == 1):
            self.img.source = 'Images/FIRSTNewton2Logo-Instructions.png'
        else:
            self.img.source = 'Images\\FIRSTNewton2Logo-Instructions.png'        
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
        self.window.add_widget(self.img)
        self.window.add_widget(self.label1)
        self.window.add_widget(self.label2)
        #endregion

    def Just_Save(self):
        self.users_df.to_csv('checkins.csv', index=False)

    def Just_Load(self):
        try:
            self.users_df = pd.read_csv('checkins.csv')
        except:
            self.users_df = self.users_df.append({'ID': "00000000", 'CIOT': "00:00:00 AM January 1, 1970", 'CIOO':0}, ignore_index=True)
        print("Checkin Dataframe: ")
        print(self.users_df)

    def Add_Checkinorout(self, ID):
        ins = 0
        outs = 0
        inorout = 0
        print(len(self.users_df))
        print(self.users_df)
        for i in range(len(self.users_df)):
            if (str(self.users_df.loc[i,'ID']) == str(ID)):
                if (self.users_df.loc[i,'CIOO'] == 1):
                    ins = ins + 1
                elif(self.users_df.loc[i,'CIOO']):
                    outs = outs + 1
        if ((ins == 0 and outs == 0)):
            inorout = 1
        else:
            if (ins > outs):
                self.users_df = self.users_df.append({'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"),'CIOO': 2}, ignore_index=True)
                inorout = 2
                Clock.schedule_once(partial(self.SplashScreen,self), 4)
                #Clock.schedule_once(partial(self.UnlockScan,self), self.sounds[self.playingSound].length + 1)
            else:
                self.users_df = self.users_df.append({'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"),'CIOO': 1}, ignore_index=True)            
                inorout = 1
        self.Just_Save()
        self.ser.flush()
        return inorout


    def MainLoop(self, *largs):
        if (self.ser.inWaiting() > 10):
            time.sleep(0.1)
            if (self.scanLock == 0):
                data = self.ReadSerial()
                data = int(data, 2)
                for i in range(len(self.user_settings_df)):                 
                    if(str(data) == str(self.user_settings_df.loc[i,'ID'])):
                        self.CheckInScreen(self.user_settings_df.loc[i,'Name'], self.user_settings_df.loc[i,'P'], self.user_settings_df.loc[i,'S'], self.user_settings_df.loc[i,'C'], self.user_settings_df.loc[i,'ID'])
                        #Clock.schedule_once(partial(self.SplashScreen,self), 10)
                        self.scanLock = 1
                        break
                else:
                    if(str(data) == ('16858422')):
                        self.PlaySound(72)
                    elif (str(data) == ('16878687')):
                        print(str(self.user_settings_df))
                        self.PlaySound(73)
                    elif (str(data) == ('16878770')):
                        print(str(self.users_df))
                        self.PlaySound(74)
                    else:
                        self.ser.write(b'4')
                        self.RogueCheckin()
                        self.PlaySound(57)    

    def Setup(self):
        #Loads encryption key into memory for future encrypting/decrypting
        with open('encryption_key.bin', 'rb') as file:
            self.encryption_key = file.read()
        self.Just_Load()

    def build(self):
        self.LoadSound() #Load all the sound file names into a list, in a specific order for posterity.        
        self.BuildElements()
        self.add_predefined_users()
        self.Setup()
        #self.window.add_widget(FirstSplashScreen(name='firstsplash'))
        if (CheckPlatform() == 1):
            Clock.schedule_interval(partial(self.MainLoop, self, 0),0.01)
        #Clock.schedule_once(partial(self.CheckInScreen,self), 9)
        return self.window

if __name__ == '__main__':
    Monolith().run()