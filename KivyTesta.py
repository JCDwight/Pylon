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


kivy.require('2.0.0') # replace with your current kivy version !

#Change to true for deployment to touchscreen
Window.fullscreen = False

sound = SoundLoader.load('PS1-Intro.wav')
if sound:
    print("Sound found at %s" % sound.source)
    print("Sound is %.3f seconds" % sound.length)
    sound.play()

#User Class
class User:
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

#
#This class defines the behavior of the check in screen
class CheckinScreen(Screen):
    checkinScreenPictureBox = ObjectProperty(None)
    def checkIn(self):
        self.checkinScreenPictureBox = Image("testa.png")

#This class defines the behavior of the splash screen
class FirstSplashScreen(Screen):
    splashScreenPictureBox = ObjectProperty(None)


#This class defines the behavior of the Window Manager
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


Builder.load_file("my.kv")



def HIDCardSwipe(self, *largs):
    sm.SwapBetweenWindows()
    #sm.current = "checkin"
    
sm = WindowManager()

class MyApp(App):
    def MainLoop(passin, *largs):
        activityTimeStamp = datetime.now()
        print('chuck testa')

    def build(self):
        sm.add_widget(FirstSplashScreen(name='firstsplash'))
        sm.add_widget(MainWindow(name='main'))
        sm.add_widget(CheckinScreen(name='checkin'))
        sm.current = 'firstsplash'
        Clock.schedule_interval(partial(self.MainLoop,'passin'),5)
        Clock.schedule_once(partial(HIDCardSwipe,self),2)
        return sm

if __name__ == '__main__':
    MyApp().run()