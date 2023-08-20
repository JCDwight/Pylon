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


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN)
pygame.display.set_caption('Monolith')
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
    #temp_sound = pygame.mixer.Sound(sound)
    #temp_sound.play()
    pass
def add_Predefined_users(user_settings_df): #Adds pre-defined users.  Will turn this into a file once I get a new user registration screen goin
    user_settings_df = add_user_settings(user_settings_df,'Coach Jay',     '44536', 7, 60,'jay.png'          ,'ORANGE')        
    user_settings_df = add_user_settings(user_settings_df,'Coach Ibrahim', '16878733', 2,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Coach Larry',   '16819201', 21,-1,'Default.png'      ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Coach Tim',     '17506192', 52,-1,'Default.png'      ,'GREEN') #16818556 old
    user_settings_df = add_user_settings(user_settings_df,'Coach Shelly',  '10497184', 72,10,'shelly.png'      ,'GOLD')
    user_settings_df = add_user_settings(user_settings_df,'Coach Renee',   '10497178', 0, 8,'renee.png'       ,'YELLOW')
    user_settings_df = add_user_settings(user_settings_df,'Coach Craig',   '16818550', 20, 0,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Coach Joe',     '10604432', 10,-1,'Default.png'     ,'PURPLE')
    user_settings_df = add_user_settings(user_settings_df,'Coach Robert',  '10497089', 41,-1,'Default.png'     ,'BLUE')
    user_settings_df = add_user_settings(user_settings_df,'Coach Charles', '50444699', 22,-1,'Default.png'     ,'CYAN')
    user_settings_df = add_user_settings(user_settings_df,'Coach Kevin',   '44094159', 79,80,'UndercoverBrother.png','RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Mary',    '10497199', 11,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Jesse',   '11118802', 50,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Lisa',    '33637371',  1,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Paul',    '88888888', 40,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Chris',   '16818544',  61,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Sam',     '9280044',  30,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Max',     '88888888',  70,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Kaitlyn', '88888888',  31,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Cassie',  '12714739',  72,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Brandon', '12744885',  32,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Keith',   '12744873',  62,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Abraham',       '88888888',  5,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Ada',           '39382',  6,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Alex',          '16878715', 7,-1,'Default.png',    'PURPLE')
    user_settings_df = add_user_settings(user_settings_df,'Aneesh',        '39360',  8,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Aryan',         '16878794', 9, 4,'thisthing.png'   ,'BLUE') #16878794 old
    user_settings_df = add_user_settings(user_settings_df,'Austin',        '16878724', 15,-1,'Default.png'     ,'GOLD')
    user_settings_df = add_user_settings(user_settings_df,'Caitlyn',       '39387',  16,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Emma',          '16858354', 17,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Evan',          '16878758', 18, 2,'EvaninFTCBox.png','RED')
    user_settings_df = add_user_settings(user_settings_df,'Hisham',        '39371',  19,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Jared',         '39339',  25,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Juliet',        '39341',  26,-1,'Default.png',    'PINK')
    user_settings_df = add_user_settings(user_settings_df,'Keita',         '16878838', 27,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Liam',          '16878885', 28,-1,'Default.png'     ,'BLUE')
    user_settings_df = add_user_settings(user_settings_df,'Luke',          '16878745', 29,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Madison',       '39301',  35,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Manav',         '39315',  36,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Martin',        '31378636', 37, 6,'Chargedup.png'   ,'CYAN')
    user_settings_df = add_user_settings(user_settings_df,'Naaisha',       '88888888',  38,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Nathan',        '16878802', 39,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Rebagrace',     '16878861', 45,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Roshan',        '88888888', 46,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Ryan',          '16878705', 47,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Sreeya',        '39362',  48,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Tejas',         '39390',  49,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Vikas',         '16878849', 55,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Xavier',        '39303',  56,-1,'Default.png',    'RED')
    return user_settings_df


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

def display_centered_text(screen, message, position=(0, 0), font_size=36, color=(255, 255, 255), font_name=None):
    """
    Display a message centered at (x, y) on the screen.

    Parameters:
    - message (str): The text to be displayed.
    - x, y (int): The center coordinates where the text should be displayed.
    - font_size (int): Size of the font to be used.
    - color (tuple): RGB tuple for the color of the text.
    - font_name (str, optional): Name of the font or path to the font file. If None, a default font will be used.
    """
    font = pygame.font.Font(font_name, font_size)  # Use None for pygame's default font
    text_surface = font.render(message, True, color)
    
    # Compute the top-left corner of the text to ensure (x, y) is at the center
    text_rect = text_surface.get_rect(center=position)
    
    screen.blit(text_surface, text_rect)

#Checks ser for nre data then returns it
def ReadSerial(ser):
    if ser.isOpen():
        try:
            if (ser.inWaiting() > 0):
                data_str = ser.read(ser.inWaiting()).decode('ascii')
                print("______________________________________")
                print("Data:")
                print((data_str))
                print("______________________________________")
                cleaned_num_str = data_str[:5]
                cleaned_num_str = int(cleaned_num_str)
                return cleaned_num_str
        except UnicodeDecodeError as e:
            print(e)
            return "0"  
        
def CheckInOutScreen(screen,inorout, name, imageFilePath, soundNum, color, ID, MPIB):
    screen.fill((0,0,0))
    display_centered_text(screen,name,(400,100),72,RED,None)
    if (inorout):
        display_centered_text(screen,'Checked in at: ' + datetime.datetime.now().strftime("%I:%M:%S %p"),(400,200),72,RED,None)
    else:
        display_centered_text(screen,'Checked out at: ' + datetime.datetime.now().strftime("%I:%M:%S %p"),(400,200),72,RED,None)
    pygame.display.flip()    
    pass

#Function to process any serial data we receive.  Should handle bad data/incomplete data
def Process_Serial_Data(ser_data,user_settings_df, screen):
    if (ser_data):
        for i in range(len(user_settings_df)):
            if(str(ser_data) == str(user_settings_df.loc[i,'ID'])):
                print('Got to before check in screen')
                #post a new pygame event.  Name first, then any parameters you want to pass in
                PlaySound('Audio/arpeggio-467.mp3')
                pygame.event.post(pygame.event.Event(ID_GET, ID_NUM=ser_data,TIME_STAMP=datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y")))
                break
        else:
            
            if(str(ser_data) == ('16858422')):
                pass
            elif (str(ser_data) == ('16878687')):
                pass
            else:
                PlaySound('Audio/i-saw-you-374.mp3')



def Add_Checkinorout(screen, checkin_df,user_settings_df, ID):
    inorout = False
    for i in range(len(checkin_df)-1, -1, -1):
        if checkin_df.at[i, 'CIOO'] == True:
            tempname = "Error"
            for j in range(len(user_settings_df)):
                if(str(ID) == str(user_settings_df.loc[j,'ID'])):
                    tempname = user_settings_df.loc[j,'Name']
                    break
            inorout = False
            print(tempname, ' has checked out')
            new_data = pd.DataFrame([{'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"), 'CIOO': False}])
            CheckInOutScreen(screen, inorout, tempname, user_settings_df.loc[i,'Picture'], user_settings_df.loc[i,'Sound'], user_settings_df.loc[i,'Color'], user_settings_df.loc[i,'ID'],user_settings_df.loc[i,'MPIB'])
            print('Name: ', )
        else:
            tempname = "Error"
            for j in range(len(user_settings_df)):
                if(str(ID) == str(user_settings_df.loc[j,'ID'])):
                    tempname = user_settings_df.loc[j,'Name']
                    break
            inorout = True
            print(ID, ' has checked in')
            new_data = pd.DataFrame([{'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"), 'CIOO': True}])
            CheckInOutScreen(screen, inorout, tempname, user_settings_df.loc[i,'Picture'], user_settings_df.loc[i,'Sound'], user_settings_df.loc[i,'Color'], user_settings_df.loc[i,'ID'],user_settings_df.loc[i,'MPIB'])
        checkin_df = pd.concat([checkin_df, new_data], ignore_index=True)
        break
    else:
        tempname = "Error"
        for j in range(len(user_settings_df)):
            if(str(ID) == str(user_settings_df.loc[j,'ID'])):
                tempname = user_settings_df.loc[j,'Name']
                break
        inorout = True
        print(ID, ' has checked in')
        new_data = pd.DataFrame([{'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"), 'CIOO': True}])
        checkin_df = pd.concat([checkin_df, new_data], ignore_index=True)
        CheckInOutScreen(screen, inorout, tempname, user_settings_df.loc[i,'Picture'], user_settings_df.loc[i,'Sound'], user_settings_df.loc[i,'Color'], user_settings_df.loc[i,'ID'],user_settings_df.loc[i,'MPIB'])

    Just_Save(checkin_df,'checkins2.csv')
    ser.flush()
    return checkin_df

def Just_Save(checkin_df, path):
    checkin_df.to_csv(path, index=False)

def Just_Load(checkin_df, path):
    try:
        checkin_df = pd.read_csv(path)
        return checkin_df
    except:
        if (path == 'checkins2.csv'):
            pass
            #checkin_df = checkin_df.append({'ID': "00000000", 'CIOT': "00:00:00 AM January 1, 1970", 'CIOO':False}, ignore_index=True)

def add_user_settings(user_settings_df, name, ident, MPIBID, s, p, c):
    new_data = pd.DataFrame([{'Name': name, 'ID': ident, 'MPIB': MPIBID, 'Sound': s, 'Picture': p, 'Color': c}])
    user_settings_df = pd.concat([user_settings_df, new_data], ignore_index=True)
    return user_settings_df

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
    checkin_df = Just_Load(checkin_df,'checkins2.csv')
    user_settings_df = add_Predefined_users(user_settings_df)
    idle = time.perf_counter() - 6
    splashimage = pygame.image.load("Images/FIRSTNewton2Logo-Instructions.png")
    while running:
        #Check Serial connection
        if (CheckPlatform() == 1):
            #print('Bits waiting: ', str(ser.inWaiting()))
            if (ser.inWaiting() >= 3):
                print(str(ser.inWaiting()))
                time.sleep(0.1)
                ser_data = ReadSerial(ser)
                ser.flush()
                if (ser_data):
                    #ser_data = str(ser_data)
                    Process_Serial_Data(ser_data, user_settings_df,screen)
        elapsed_time = time.perf_counter() - idle
        if (elapsed_time > 5 and elapsed_time < 7):
            screen.fill((0,0,0))
            screen.blit(splashimage, (0, 0))
            pygame.display.flip()

        for event in pygame.event.get():           
            if(event.type == ID_GET):
                checkin_df = Add_Checkinorout(screen, checkin_df,user_settings_df,event.ID_NUM)
                idle = time.perf_counter()
            elif(event.type == pygame.QUIT):
                running = False
                pygame.quit()
                sys.exit()
        #clock.tick(60)




        