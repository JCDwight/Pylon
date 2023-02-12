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
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


kivy.require('2.0.0') # replace with your current kivy version !

Window.fullscreen = False

from kivy.app import App
from kivy.uix.label import Label

wimg = Image(source='jay.png')
wimg = Image(source='newtonsquared.png')


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

class CheckinScreen(Screen):
    pass

class FirstSplashScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MainWindow(Screen):
    flag1 = 0
    pictureBox = ObjectProperty(None)
    pictureBox2 = ObjectProperty(None)
    pictureBox3 = ObjectProperty(None)

    def btn(self):
        print(Window.mouse_pos)
        if(self.flag1 == 0):
            ani = Animation(opacity=0,duration=0.25)
            ani.start(self.pictureBox)
            self.flag1 = 1
        else:
            ani = Animation(opacity=1,duration=0.25)
            ani.start(self.pictureBox)
            self.flag1 = 0

kv = Builder.load_file("my.kv")

class MyApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    MyApp().run()