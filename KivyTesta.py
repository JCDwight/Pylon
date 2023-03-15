from winsound import PlaySound
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
from functools import partial
import pandas 
import time


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

#Builder.load_file("my.kv")

def HIDCardSwipe(self, *largs):
    sm.SwapBetweenWindows()
    #sm.current = "checkin"
    
sm = WindowManager()

#Sound Loaders
#region Sound Loaders
#Sound loaders.  Loading sounds at the beginning of the file allows them to be played in runtime with no delay
#sound_ = SoundLoader.load("Audio\\.wav")
#sound_PS1 = SoundLoader.load("Audio\\PS1-Intro.wav")
#sound_JohnCena = SoundLoader.load("Audio\\JohnCena.wav")
#sound_FlashSavioroftheUniverse = SoundLoader.load("Audio\\FlashSavioroftheUniverse.wav")
#endregion

class MyApp(App):
    #START Application Variables
    users = []
    sounds = []
    #END   Application Variables
    def LoadSound(self):
        #region
        self.sounds.append(SoundLoader.load("Audio\\PS1-Intro.wav"))        
        self.sounds.append(SoundLoader.load("Audio\\JohnCena.wav"))
        self.sounds.append(SoundLoader.load("Audio\\FlashSavioroftheUniverse.wav"))
        #endregion

    def PlaySound(self):
        selector = 0
        if (self.sounds[selector]):
            self.sounds[selector].play()
            print("I got here")

    def LoadUsers():
        pass

    def MainLoop(self, *largs):
        print('Check testa')
        flag = 0
        self.PlaySound()
        pass

    def build(self):
        self.LoadSound()
        sm.add_widget(FirstSplashScreen(name='firstsplash'))
        sm.add_widget(MainWindow(name='main'))
        sm.add_widget(CheckinScreen(name='checkin'))
        sm.current = 'firstsplash'
        Clock.schedule_interval(partial(self.MainLoop, self, 2),5)
        Clock.schedule_once(partial(HIDCardSwipe,self),2)
        return sm

if __name__ == '__main__':
    MyApp().run()