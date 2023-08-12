import platform as plat
import pygame
import sys
import time
import serial
import datetime
import pandas as pd

pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# Basic Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Extended Colors
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
SILVER = (192, 192, 192)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
GOLD = (255, 215, 0)
LIME = (50, 205, 50)
LAVENDER = (230, 230, 250)
BEIGE = (245, 245, 220)
AQUA = (0, 255, 255)
CORAL = (255, 127, 80)
INDIGO = (75, 0, 130)
IVORY = (255, 255, 240)
KHAKI = (240, 230, 140)
VIOLET = (238, 130, 238)
WHEAT = (245, 222, 179)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple UI in Pygame')
clock = pygame.time.Clock()

#Checks the platform the program is running on.  Returns: Linux = 1, Windows = 2, everything else is 3
def CheckPlatform():
    if (plat.platform()[0] == "L" or plat.platform()[0] == "l"):
        return 1
    elif (plat.platform()[0] == "W" or plat.platform()[0] == "w"):
        return 2
    else:
        return 3

#Loads and plays a sound via pygame mixer   
def PlaySound(sound):
    temp_sound = pygame.mixer.Sound(sound)
    temp_sound.play()

def add_Predefined_users(user_settings_df): #Adds pre-defined users.  Will turn this into a file once I get a new user registration screen goin
    add_user_settings(user_settings_df,'Coach Jay',     '16819214', 7, 1,'jay.png'          ,'ORANGE')        
    add_user_settings(user_settings_df,'Jackson',       '16878869', 78,-1,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Liam',          '16878885', 32,-1,'Default.png'     ,'BLUE')
    add_user_settings(user_settings_df,'Luke',          '16878745', 52,-1,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Ibrahim',       '16878733', 77,-1,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Ryan',          '16878705', 41,-1,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Rebagrace',     '16878861', 37,-1,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Coach Larry',   '16819201', 3,-1,'Default.png'      ,'GREEN')
    add_user_settings(user_settings_df,'Coach Harrison','16818556', 18,-1,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Coach Tim',     '17506192', 6,-1,'Default.png'      ,'GREEN') #16818556 old
    add_user_settings(user_settings_df,'Cole',          '16878693', 76,-1,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Martin',        '31378636', 20, 6,'Chargedup.png'   ,'CYAN')
    add_user_settings(user_settings_df,'Coach Shelly',  '10497184', 16,10,'shelly.png'      ,'GOLD')
    add_user_settings(user_settings_df,'Evan',          '16878758', 36, 2,'EvaninFTCBox.png','RED')
    add_user_settings(user_settings_df,'Coach Renee',   '10497178', 0, 8,'renee.png'       ,'YELLOW')
    add_user_settings(user_settings_df,'Aryan',         '16878794', 21, 4,'thisthing.png'   ,'BLUE') #16878794 old
    add_user_settings(user_settings_df,'Keita',         '16878838', 27,-1,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Annabelle',     '16878841', 22,-1,'Default.png'     ,'PURPLE')
    add_user_settings(user_settings_df,'Austin',        '16878724', 51,-1,'Default.png'     ,'GOLD')
    add_user_settings(user_settings_df,'Ted',           '16878757', 00,20,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Coach Craig',   '16818550', 2, 0,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Susan',         '16858448', 00,-1,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Ty',            '10518941', 75,75,'Tytaco.png'      ,'ORANGE')    
    add_user_settings(user_settings_df,'Emma',          '16858354', 43,-1,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Vikas',         '16878849', 29,-1,'Default.png'     ,'GREEN')
    add_user_settings(user_settings_df,'Coach Joe',     '10604432', 10,-1,'Default.png'     ,'PURPLE')
    add_user_settings(user_settings_df,'Megan',         '16878711', 75,-1,'Default.png'     ,'PURPLE')
    add_user_settings(user_settings_df,'Chris',         '16878807', 74,-1,'Default.png'     ,'PURPLE')
    add_user_settings(user_settings_df,'Coach Robert',  '10497089', 12,-1,'Default.png'     ,'BLUE')
    add_user_settings(user_settings_df,'Coach Charles', '50444699', 9,-1,'Default.png'     ,'CYAN')
    add_user_settings(user_settings_df,'Coach Kevin',   '44094159', 70,80,'UndercoverBrother.png','RED')
    add_user_settings(user_settings_df,'Alex',          '16878715', 35,-1,'Default.png',    'PURPLE')
    add_user_settings(user_settings_df,'Nathan',        '16878802', 53,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Coach Mary',    '10497199',  11,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Coach Jesse',   '11118802',  5,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Coach Lisa',    '33637371',  1,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Coach Paul',    '88888888',  4,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Coach Chris',   '16818544',  8,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Coach Sam',     '9280044',  13,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Coach Max',     '88888888',  14,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Coach Kaitlyn', '88888888',  15,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Coach Cassie',  '12714739',  17,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Coach Brandon', '12744885',  17,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Coach Keith',   '12744873',  17,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Juliet',        '1639341',  22,-1,'Default.png',    'PINK')
    add_user_settings(user_settings_df,'Madison',       '1639301',  23,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Sreeya',        '1639362',  25,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Aneesh',        '1639360',  26,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Naaisha',       '88888888',  28,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Abraham',       '88888888',  40,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Tejas',         '1639390',  42,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Xavier',        '1639303',  30,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Jared',         '1639339',  31,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Hisham',        '1639371',  38,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Caitlyn',       '1639387',  39,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Manav',         '1639315',  44,-1,'Default.png',    'RED')
    add_user_settings(user_settings_df,'Ada',           '1639326',  50,-1,'Default.png',    'RED')



#Displays text on the screen
def display_text(screen, text, position=(0, 0), size=36, color=(255, 255, 255), font_name=None):
    """
    Display text on the pygame screen.

    Parameters:
    - screen: The pygame surface where the text will be displayed.
    - text: The text string to display.
    - position: A tuple (x, y) representing the position on the screen to start displaying the text. Default is (0, 0).
    - size: Font size. Default is 36.
    - color: A tuple (R, G, B) representing the color of the text. Default is white.
    - font_name: Name or path of the font to use. If None, pygame's default font will be used. Default is None.
    """
    
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

#Checks ser for nre data then returns it
def ReadSerial(ser):
    if ser.isOpen():
        try:
            if (ser.inWaiting() > 0):
                data_str = ser.read(ser.inWaiting()).decode('ascii')
                print("______________________________________")
                print("Data 2: ", data_str)
                print("Data:")
                print(int(data_str, 2))
                print("______________________________________")
                return data_str
        except UnicodeDecodeError as e:
            print(e)
            return "0"  
        
#Function to process any serial data we receive.  Should handle bad data/incomplete data
def Process_Serial_Data(ser_data):
    if (ser_data):
        #post a new pygame event.  Name first, then any parameters you want to pass in
        pygame.event.post(pygame.event.Event(ID_GET, ID_NUM=str(ser_data)))

def Add_Checkinorout(users_df,ID):
    ins = int(0)
    outs = int(0)
    inorout = 0
    for i in range(len(users_df)):
        if (str(users_df.loc[i,'ID']) == str(ID)):
            if (users_df.loc[i,'CIOO'] == True):
                ins = ins + 1
            elif(users_df.loc[i,'CIOO'] == False):
                outs = outs + 1
    if ((ins == 0 and outs == 0)):
        print("Added check-in")
        users_df = users_df.append({'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"),'CIOO': True}, ignore_index=True)            
        inorout = int(1)
    else:
        if (ins > outs):
            users_df = users_df.append({'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"),'CIOO': False}, ignore_index=True)
            print("Added check-out")
            inorout = int(2)
            #Clock.schedule_once(partial(self.SplashScreen,self), 5.5)

        else:
            print("Added check-in")
            #Clock.schedule_once(partial(self.SplashScreen,self), 5.5)
            users_df = users_df.append({'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"),'CIOO': True}, ignore_index=True)            
            inorout = int(1)
    #Just_Save('checkins.csv')
    ser.flush()
    return inorout

def add_user_settings(user_settings_df, name, ident, MPIBID, s, p, c):
    user_settings_df = user_settings_df.append({'Name': name, 'ID': ident,'MPIB': MPIBID, 'S': s, 'P': p, 'C': c}, ignore_index=True)

if __name__ == '__main__':
    #Define passable variables
    checkin_df = pd.DataFrame(columns=['ID', 'CIOT', 'CIOO'])
    user_settings_df = pd.DataFrame(columns=['Name', 'ID', 'MPIB', 'Sound', 'Picture', 'Color'])
    #Use Checkplatform to check if we're on Linux(For production) or Windows(For testing)
    #and set parameters for each
    if (CheckPlatform() == 1):
        #1 == Linux, enable serial functions
        print('Opening serial port... at 500,000 baud')
        ser = serial.Serial('/dev/ttyACM0', 500000)
    elif (CheckPlatform() == 2):
        #2 == Windows, disable serial functions
        pass
    else:
        #Anything else, set lowest defaults because we don't know what OS is running
        pass
    #Set Pygame custom events to handle Monolith specific events.  Increment the integer for each new one
    ID_GET = pygame.USEREVENT + 1
    #Set our main loop variable to true, while true the program will run forever
    running = True
    while running:
        #Check Serial connection
        if (CheckPlatform() == 1):
            ser_data = ReadSerial(ser)
            Process_Serial_Data(ser_data)
        for event in pygame.event.get():           
            if(event.type == ID_GET):
                temp = event.ID_NUM
                print(str(temp))
            elif(event.type == pygame.QUIT):
                running = False
                pygame.quit()
                sys.exit()
        clock.tick(60)




        