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
from kivy.config import Config
from datetime import datetime
import subprocess
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
import random
import sys
import shutil
import csv
import socket

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

kivy.require('2.0.0') # replace with your current kivy version !
FULL_SCREEN = 0
#Change to true for deployment to touchscreen
MPIB_Status = ""
update_MPIB = ""

def handle_client(conn):
    global update_MPIB
    global MPIB_Status
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received data: {data.decode('utf-8')}")
        rdata = data
        print(str(rdata))
        if rdata == b"update":
            if not(update_MPIB == ""):
                response = update_MPIB
                update_MPIB = ""
            else:
                response = "No"    
            conn.send(response.encode('utf-8'))
        elif(rdata == b"refresh"):
            response=""
            for i in range(60):
                response = response + str(i) + ",RED|"
                #response = "16,RED|17,BLUE|18,GREEN|19,RED|20,BLUE|21,GREEN|22,RED|23,BLUE|24,GREEN"
            print(str(response))
            conn.send(response.encode('utf-8'))
            update_MPIB = ""
    conn.close()

def start_server(host='10.42.0.201', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # This line enables port reusage:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server started!! Listening at {host}:{port}")

    while True:
        conn, address = server_socket.accept()
        print(f"Connection from {address}")
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()



# The rest of your application can go here



def CheckPlatform():
    #Checks the platform the program is running on.  Linux = 1, Windows = 2, everything else is 3
    if (plat.platform()[0] == "L" or plat.platform()[0] == "l"):
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
    user_settings_df = pd.DataFrame(columns=['Name', 'ID', 'MPIB', 'S', 'P', 'C'])
    unauthorized_users_df = pd.DataFrame(columns=['ID', 'CIOT'])
    encryption_key = 0
    encrypted_data = 0
    clean_up = 1
    backedup = 0
    sound_on = True

    #END   Application Variables

    if (CheckPlatform() == 1):
        print('Opening serial port...')
        ser = serial.Serial('/dev/ttyACM0', 500000)

    if (CheckPlatform() == 2):
        print('Opening serial port...')
        #ser = serial.Serial('COM8', 500000)

    def add_user_settings(self, name, ident, MPIBID, s, p, c):
        self.user_settings_df = self.user_settings_df.append({'Name': name, 'ID': ident,'MPIB': MPIBID, 'S': s, 'P': p, 'C': c}, ignore_index=True)

    def add_rogue_user(self):
        pass

    #Intercept Rogue Checkins - Ah ah ah!  You didn't say the magioc word!
    def RogueCheckin(self):
        pass

    def save_list_to_csv(self,file_path, data):
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

    def load_csv_to_list(self,file_path):
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)[0]
        return data

    def add_predefined_users(self): #Adds pre-defined users.  Will turn this into a file once I get a new user registration screen goin
        self.add_user_settings('Coach Jay',     '16819214', 13, 1,'jay.png'         ,'Orange')
        self.add_user_settings('Chuck Testa',   '10101010', 79, 1,'ChuckTesta.png'  ,'Orange')
        self.add_user_settings('Jackson',       '16878869', 78,-1,'Default.png'     ,'Green')
        self.add_user_settings('Liam',          '16878885', 28,-1,'Default.png'     ,'Blue')
        self.add_user_settings('Luke',          '16878745', 00,-1,'Default.png'     ,'Green')
        self.add_user_settings('Ibrahim',       '16878733', 77,-1,'Default.png'     ,'Green')
        self.add_user_settings('Ryan',          '16878705', 31,-1,'Default.png'     ,'Green')
        self.add_user_settings('Rebagrace',     '16878861', 30,-1,'Default.png'     ,'Green')
        self.add_user_settings('Coach Larry',   '16819201', 3,-1,'Default.png'     ,'Green')
        self.add_user_settings('Coach Harrison','16818556', 00,-1,'Default.png'     ,'Green')
        self.add_user_settings('Coach Tim',     '16818556', 2,-1,'Default.png'     ,'Green')
        self.add_user_settings('Cole',          '16878693', 76,-1,'Default.png'     ,'Green')
        self.add_user_settings('Martin',        '16858425', 20, 6,'Chargedup.png'   ,'Cyan')
        self.add_user_settings('Coach Shelly',  '10497184', 12,10,'shelly.png'      ,'Gold')
        self.add_user_settings('Evan',          '16878758', 26, 2,'EvaninFTCBox.png','Red')
        self.add_user_settings('Coach Renee',   '10497178', 10, 8,'renee.png'       ,'Yellow')
        self.add_user_settings('Aryan',         '16878794', 23, 4,'thisthing.png'   ,'Blue')
        self.add_user_settings('Keita',         '16878838', 27,-1,'Default.png'     ,'Green')
        self.add_user_settings('Annabelle',     '16878841', 22,-1,'Default.png'     ,'Purple')
        self.add_user_settings('Austin',        '16878724', 00,-1,'Default.png'     ,'Gold')
        self.add_user_settings('Ted',           '16878757', 00,20,'Default.png'     ,'Green')
        self.add_user_settings('Coach Craig',   '16818550', 4, 0,'Default.png'     ,'Green')
        self.add_user_settings('Susan',         '16858448', 00,-1,'Default.png'     ,'Green')
        self.add_user_settings('Ty',            '10518941', 75,75,'Tytaco.png'      ,'Orange')    
        self.add_user_settings('Emma',          '16858354', 25,-1,'Default.png'     ,'Green')
        self.add_user_settings('Vikas',         '16878849', 32,-1,'Default.png'     ,'Green')
        self.add_user_settings('Coach Joe',     '10604432', 00,-1,'Default.png'     ,'Purple')
        self.add_user_settings('Megan',         '16878711', 75,-1,'Default.png'     ,'Purple')
        self.add_user_settings('Chris',         '16878807', 74,-1,'Default.png'     ,'Purple')
        self.add_user_settings('Coach Robert',  '10497089', 8,-1,'Default.png'     ,'Blue')
        self.add_user_settings('Coach Charles', '50444699', 7,-1,'Default.png'     ,'Cyan')
        self.add_user_settings('Coach Kevin',   '44094159', 00,80,'UndercoverBrother.png','Red/Yellow/Green')
        self.add_user_settings('Alex',          '16878715', 21,-1,'Default.png',    'Purple')
        self.add_user_settings('Nathan',        '16878802', 00,-1,'Default.png',    'Red')

    def LoadSound(self):
        #region
        #
        loadFile = []
        noFile = False #Set noFile to false, if we can not load the file we will set this to true
        dir_list = 0
        path = "Audio\\" #Folder in the root directory that holds all our audio files
        if (CheckPlatform() == 1):
            dir_list = os.listdir("Audio") #Use the OS library to scan the directory for all files and store them in dir_list
        elif (CheckPlatform() == 2):
            dir_list = os.listdir(path) #Use the OS library to scan the directory for all files and store them in dir_list
        try: #Use exception handling in case the file does not exist
            loadFile = self.load_csv_to_list('DataBases/audioFiles.csv') #Try to load audioFiles.csv
        except: #If no file exists, we set noFile to true and will create one with the scanned directory.  This should only happen once on first run.
            noFile = True
                                #A file already exists, so we need to load in any new files to the end of the list
        if (noFile == False):   #if we loaded them in the dir_list order it would change a user's selected file
            fallThrough = False
            newlist = []
            for g in range(len(loadFile)):
                newlist.append(loadFile[g])
            for g in range(len(newlist)):
                listItem = newlist[g]
                listItem = str(listItem)            #g starts as a list, we need to convert it to a string
                self.soundList.append(listItem)
            for f in range(len(dir_list)):
                flagged = False
                for g in range(len(newlist)):
                    listItem = newlist[g]
                    listItem = str(listItem)            #g starts as a list, we need to convert it to a string

                    if ((dir_list[f] == listItem) and (flagged == False)): #If the files in the scanned dir_list match the old list, flag and skip
                        fallThrough = False
                        flagged = True
                        break
                    else:
                        fallThrough = True #If they don't match, fallthrough so we add it to the list
                if ((fallThrough) and (flagged == False)): #Add new sound to list if fallThrough == True and Flagged(As a match) == False
                    self.soundList.append(dir_list[f])
            self.save_list_to_csv('DataBases/audioFiles.csv',self.soundList)
        else:
            for f in dir_list: #No file exists, so just dump the scanned directory files into a list, should happen 1x
                self.soundList.append(f)
            self.save_list_to_csv('DataBases/audioFiles.csv',self.soundList)
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
            self.PlaySound(random.randint(1,50))
        #endregion

    def UnlockScan(self, *largs):
        print("Unlocked scan")
        self.scanLock = 0

    def PlaySound(self, selector):
        #region
        if (self.sound_on):
            t = round(time.time() * 1000)
            #    If self.sounds[selector] exists, AND The length of the playing sound is less than the current time sound has been playing, then play the new sound
            #print (self.sounds)
            if ((self.sounds[selector]) and ((self.sounds[self.playingSound].length * 1000) < t - self.soundTime)): 
                self.sounds[selector].play() #Plays the selected sound
            #ps.playsound("Audio//" + self.soundList[selector], False)
            self.playingSound = selector #Save the current selected song as our playing sound, since we made it in here, and the sound is playing
            self.scanLock = 1
            print("Length of audio file: " + str(self.sounds[self.playingSound].length))
            Clock.schedule_once(partial(self.SplashScreen,self), self.sounds[self.playingSound].length + 1)
            self.soundTime = round(time.time() * 1000) #get the time, round it, and multiply it by 1000 to convert to milliseconds
            #endregion

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

    def Set_MPIB_Status_Global(self):
        tempstr = ""
        exclude = []
        exclude.append("00000000")
        for i in range(len(self.users_df),-1,-1): #Iterate backwards through scheckin DB
            if exclude: #If an exclude list exists
                for j in exclude: #For each item in the exclude list
                    if (str(self.users_df.loc[i,'ID']) == str(j)): #Check if the checkin DB matches
                        pass                                       #an existing ID in the exclude list
                    else:
                        temploc = ""
                        tempcolor = ""
                        for l in range(len(self.user_settings_df)):#Looks through settings DB to match the ID and find the MPIB ID
                            if (str(self.user_settings_df.loc[l,'ID']) == str(self.users_df.loc[i,'ID'])):
                                temploc = self.user_settings_df.loc[l,'MPIB']
                        if (self.users_d.loc[i,'CIOO'] == 1): #Check if in and assign color
                            tempcolor = "GREEN"
                        if (self.users_d.loc[i,'CIOO'] == 2): #Check if out and assign color
                            tempcolor = "RED"
                        tempstr = tempstr + str(temploc,",",tempcolor,"|")
            exclude = exclude.append(str(self.users_df.loc[i,'ID']))
        MPIB_Status = tempstr

                        

    def CheckInScreen(self, name, imageFilePath, soundNum, color, ID, MPIB):
        global update_MPIB
        if (CheckPlatform() == 1):
            self.ser.write(b'3')
        if (CheckPlatform() == 1):
            self.ser.flush()
        inorout = self.Add_Checkinorout(ID)
        if (soundNum > -1 and inorout == 1):
            pass
            #self.PlaySound(soundNum)
        elif(soundNum < 0 and inorout == 1):
            pass
            #self.PlaySound(random.randint(58,69))
        if (inorout == 1):
            self.label1.text = name + ' checked in!'
            update_MPIB = str(MPIB) + ",GREEN"
        else:
            self.label1.text = name + ' checked out!'
            update_MPIB = str(MPIB) + ",RED"
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
        print("Got to the end of check in/out")
        Set_MPIB_Status_Global()

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

    def upload_picture_to_drive(picture_path, drive_folder_id):
        credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/drive'])

        drive_service = build('drive', 'v3', credentials=credentials)
        
        file_metadata = {
            'name': 'picture.jpg',
            'parents': [drive_folder_id]
        }

        media = MediaFileUpload(picture_path, mimetype='image/jpeg')

        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print('Picture uploaded. File ID:', file.get('id'))

    def Just_Save(self, path):
        self.users_df.to_csv(path, index=False)
        #print("Saved checkins")

    def Just_Load(self, path):
        try:
            self.users_df = pd.read_csv(path)
        except:
            if (path == 'checkins.csv'):
                self.users_df = self.users_df.append({'ID': "00000000", 'CIOT': "00:00:00 AM January 1, 1970", 'CIOO':0}, ignore_index=True)
            elif (path == 'unauthorized.csv'):
                self.unauthorized_users_df = self.unauthorized_users_df.append({'ID': "00000000", 'CIOT': "00:00:00 AM January 1, 1970"}, ignore_index=True)

        #print("Checkin Dataframe: ")
        #print(self.users_df)

    def Add_Checkinorout(self, ID):
        ins = 0
        outs = 0
        inorout = 0
        #print(len(self.users_df))
        #print(self.users_df)
        for i in range(len(self.users_df)):
            if (str(self.users_df.loc[i,'ID']) == str(ID)):
                if (self.users_df.loc[i,'CIOO'] == 1):
                    ins = ins + 1
                elif(self.users_df.loc[i,'CIOO']):
                    outs = outs + 1
        if ((ins == 0 and outs == 0)):
            print("Added check-in")
            self.users_df = self.users_df.append({'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"),'CIOO': 1}, ignore_index=True)            
            inorout = 1
        else:
            if (ins > outs):
                self.users_df = self.users_df.append({'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"),'CIOO': 2}, ignore_index=True)
                print("Added check-out")
                inorout = 2
                Clock.schedule_once(partial(self.SplashScreen,self), 4)
                #Clock.schedule_once(partial(self.UnlockScan,self), self.sounds[self.playingSound].length + 1)
            else:
                print("Added check-in")
                Clock.schedule_once(partial(self.SplashScreen,self), 4)
                self.users_df = self.users_df.append({'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"),'CIOO': 1}, ignore_index=True)            
                inorout = 1
        self.Just_Save('checkins.csv')
        self.ser.flush()
        return inorout
    
    def git_pull():
        try:
            output = subprocess.check_output(['git', 'pull'], stderr=subprocess.STDOUT)
            print(output.decode())
        except subprocess.CalledProcessError as e:
            print(f'Error: {e.output.decode()}')

    def Print_Checkins_With_Names(self):
        for i in range(self.users_df.shape[0]):
            for j in range(self.user_settings_df.shape[0]):
                if (str(self.users_df.loc[i,'ID']) == str(self.user_settings_df.loc[j,'ID'])): 
                    if (self.users_df.loc[i,'CIOO']) == 1:
                        print(str(self.user_settings_df.loc[j,'Name']) + ' - ' + str(self.users_df.loc[i,'CIOT']) + ' - ' + "In")
                    if (self.users_df.loc[i,'CIOO']) == 2:
                        print(str(self.user_settings_df.loc[j,'Name']) + ' - ' + str(self.users_df.loc[i,'CIOT']) + ' - ' + "Out")

    def MainLoop(self, *largs):
        if (self.ser.inWaiting() > 10):
            time.sleep(0.1)
            if (self.scanLock == 0):
                data = self.ReadSerial()
                data = int(data, 2)
                for i in range(len(self.user_settings_df)):
                    if(str(data) == str(self.user_settings_df.loc[i,'ID'])):
                        self.CheckInScreen(self.user_settings_df.loc[i,'Name'], self.user_settings_df.loc[i,'P'], self.user_settings_df.loc[i,'S'], self.user_settings_df.loc[i,'C'], self.user_settings_df.loc[i,'ID'],self.user_settings_df.loc[i,'MPIB'])
                        Clock.schedule_once(partial(self.SplashScreen,self), 10)
                        self.scanLock = 0
                        break
                else:
                    if(str(data) == ('16858422')):
                        pass
                        #self.PlaySound(72)
                    elif (str(data) == ('16878687')):
                        print(str(self.user_settings_df))
                        #self.PlaySound(73)
                    elif (str(data) == ('16858416')):
                        if (self.sound_on):
                            self.sound_on = False
                        else:
                            self.sound_on = True
                    elif (str(data) == ('16878770')):
                        #print(str(self.users_df))
                        #self.Print_Checkins_With_Names()
                        self.CheckEveryoneOut()
                        #self.PlaySound(78)
                    else:
                        self.ser.write(b'4')
                        #self.unauthorized_users_df = self.unauthorized_users_df.append({'ID': str(data), 'CIOT': datetime.datetime.now().strftime("%I:%M %p\n %B %d, %Y")})
                        #unauthorizedcheckins = 0
                        #for checkin in self.unauthorized_users_df:
                        #    if(checkin['ID'] == str(data)):
                        #        unauthorizedcheckins = unauthorizedcheckins + 1
                        #if(unauthorizedcheckins > 0 and unauthorizedcheckins < 5):
                        #self.PlaySound(57)
                        #elif(unauthorizedcheckins < 10):
                        #    pass
                        #elif(unauthorizedcheckins < 11):
                        #    pass
                        #elif(unauthorizedcheckins < 12):
                        #    pass
                        #elif(unauthorizedcheckins < 13):
                        #    pass
                        #elif(unauthorizedcheckins < 14):
                        #    pass
                        #elif(unauthorizedcheckins < 15):
                        #    pass
                        #elif(unauthorizedcheckins < 16):
                        #    pass

    def Setup(self):
        self.Just_Load('checkins.csv')
        #self.Just_Load('unauthorized.csv')

    def CheckEveryoneOut(self):
        numcolumns = self.users_df.shape[0] - 1
        print("self.users_df.shape[1]" + str(self.users_df.shape[0]))
        id_list = []
        id_list.append("00000000")
        print("ID List in the beginning: " + str(id_list))
        exclude_list = []
        exclude_list.append("00000000")
        exclude = 0
        if (self.clean_up == 1):
            for i in range(numcolumns, -1, -1):
                print("In loop: " + str(i) + " ID: " + str(self.users_df.loc[i,'ID']))
                exclude = 0
                if (self.users_df.loc[i,'CIOO'] == 1):
                    if (len(id_list) > 0):
                        for j in range(len(id_list)):
                            if (i == 85):
                                print("User DF ID: " + str(self.users_df.loc[i,'ID']) + " VS id_list: " + str(id_list[j]))
                            if (str(self.users_df.loc[i,'ID']) == str(id_list[j])):
                                print("Broke out because self.users_df.loc[i,'ID'] == id_list[j]")
                                break
                        else:
                            print("No breakout, checking exclude list")
                            if (len(exclude_list) > 0):
                                for e in range(len(exclude_list)):
                                    if (i == 85):
                                        print("User DF ID: " + str(self.users_df.loc[i,'ID']) + " VS exclude_list: " + str(exclude_list[e]))
                                    if (str(self.users_df.loc[i,'ID']) == str(exclude_list[e])):
                                        print("On excluded list")
                                        exclude = 1
                            if (exclude == 0):
                                id_list.append(str(self.users_df.loc[i,'ID']))
                                print("Appended: self.users_df.loc[i,'ID'] : " + str(self.users_df.loc[i,'ID']) + " to the id_list")
                elif (self.users_df.loc[i,'CIOO'] == 2):
                    if (len(id_list) > 0):
                        in_id_list = 0
                        for j in range(len(id_list)):
                            if (str(self.users_df.loc[i,'ID']) == str(id_list[j])):
                                in_id_list = 1
                                break
                        if(in_id_list == 0):
                            exclude_list.append(str(self.users_df.loc[i,'ID']))
            print("len(id_list) :" + str(len(id_list)))
            if (len(id_list) > 0):
                for i in range(len(id_list)):
                    if(str(id_list[i]) != "00000000"):
                        name = ""
                        for q in range(self.user_settings_df.shape[0]):
                            if(str(self.user_settings_df.loc[q,'ID']) == str(id_list[i])):
                                name = self.user_settings_df.loc[q,'Name']       
                        self.users_df = self.users_df.append({'ID': id_list[i], 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"),'CIOO': 2}, ignore_index=True)
                        print ('ID: ', str(id_list[i]), ' , CIOT: ', str(datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y")) , ' CIOO: OUT')
            self.clean_up = 0
            self.Just_Save('checkins.csv')


    def CopyFile(self, source_file, destination_file):     
        # Copy the file
        print("Copying: " + str(source_file) + " to " + str(destination_file))
        shutil.copy2(source_file, destination_file)

    def CheckTime(self,*largs):
        hour = datetime.datetime.now().strftime("%H")
        hour = int(hour)
        min = datetime.datetime.now().strftime("%M")
        min = int(min)
        if ((hour == 23) and (min == 45)):
            print("Checking everyone out")
            self.CheckEveryoneOut()
        if ((hour == 23) and (min == 55) and (self.backedup == 0)):
            self.CopyFile('checkins.csv','/Backups/checkins-' + str(datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"))
            self.users_df = {'ID': "00000000", 'CIOT': "00:00:00 AM January 1, 1970", 'CIOO':0}
            self.Just_Save('checkins.csv')
            self.backedup = 1
        if ((hour == 1) and (min == 5)):
            print("Switching Self clean up back to 1")
            self.clean_up = 1
            self.backedup = 0

    def build(self):
        self.LoadSound() #Load all the sound file names into a list, in a specific order for posterity.        
        self.BuildElements()
        self.add_predefined_users()
        self.Setup()
        
        # Start the server in a new thread
        server_thread = threading.Thread(target=start_server)
        server_thread.start()
        #self.window.add_widget(FirstSplashScreen(name='firstsplash'))
        if (CheckPlatform() == 1):
            Clock.schedule_interval(partial(self.MainLoop, self, 0),0.01)
            Clock.schedule_interval(partial(self.CheckTime, self), 20)
        #Clock.schedule_once(partial(self.CheckInScreen,self), 9)
        return self.window

if __name__ == '__main__':
    Monolith().run()
