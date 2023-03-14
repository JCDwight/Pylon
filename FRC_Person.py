import datetime
import pandas as pd

class FRC_Person:
    #attributes
    id_code = 0
    first_name = ""
    last_name = ""
    birthday = datetime.date(1970,1,1)
    gender = -1 # -1 = Invalid, 0 = Male, 1 = Female, 3 = Other
    #end attributes

    #Initialize
    def __init__(self,first_name,last_name, birthday):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday

    #Getters/Setters
    def GetFirstName(self):
        return self.first_name
    def SetFirstName(self, value):
        self.first_name = value
    def GetLastName(self):
        return self.last_name
    def SetLastName(self, value):
        self.last_name = value
    def GetBirthday(self):
        return self.birthday
    def SetBirthday(self, value):
        self.birthday = value
    def GetGender(self):
        return self.gender
    def SetGender(self, value):
        self.gender = value
    def GetAge(self):
        return (datetime.date.today() - self.birthday / 365)
    #END Getters/Setters
    #Functionality
    
    #Load information from the DB into individual Object
    def LoadInfo(self):
        pd.read_json()
        pass
    #Save information from individual Object into the DB
    def SaveInfo(self):
        pd.to_json()

        
    