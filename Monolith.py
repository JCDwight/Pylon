import platform as plat
import pygame
import sys
import time
import serial
import datetime
import pandas as pd
import socket
import threading

pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

update_MPIB = ""
refresh_MPIB = ""

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
    temp_sound = pygame.mixer.Sound(sound)
    temp_sound.play()

def add_Predefined_users(user_settings_df): #Adds pre-defined users.  Will turn this into a file once I get a new user registration screen goin
    user_settings_df = add_user_settings(user_settings_df,'Coach Jay',     '44536', 60, 60,'jay.png'          ,'ORANGE')        
    user_settings_df = add_user_settings(user_settings_df,'Coach Ibrahim', '39377', 2,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Coach Larry',   '88888888', 21,-1,'Default.png'      ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Coach Tim',     '6192', 52,-1,'Default.png'      ,'GREEN') #16818556 old
    user_settings_df = add_user_settings(user_settings_df,'Coach Shelly',  '59823', 72,10,'shelly.png'      ,'GOLD')
    user_settings_df = add_user_settings(user_settings_df,'Coach Renee',   '59826', 0, 8,'renee.png'       ,'YELLOW')
    user_settings_df = add_user_settings(user_settings_df,'Coach Craig',   '44868', 20, 0,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Coach Joe',     '6199', 10,-1,'Default.png'     ,'PURPLE')
    user_settings_df = add_user_settings(user_settings_df,'Coach Robert',  '59871', 41,-1,'Default.png'     ,'BLUE')
    user_settings_df = add_user_settings(user_settings_df,'Coach Charles', '9010', 22,-1,'Default.png'     ,'CYAN')
    user_settings_df = add_user_settings(user_settings_df,'Coach Kevin',   '88888888', 79,80,'UndercoverBrother.png','RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Mary',    '59816', 11,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Jesse',   '88888888', 50,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Lisa',    '44801',  1,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Paul',    '39347', 40,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Chris',   '88888888',  61,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Sam',     '13033',  30,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Max',     '48997',  70,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Kaitlyn', '39366',  31,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Cassie',  '14739',  72,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Brandon', '88888888',  32,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Keith',   '44873',  62,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Coach Kelsey',   '44508',  12,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Abraham',       '88888888',  5,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Ada',           '39382',  6,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Alex',          '14786', 7,-1,'Default.png',    'PURPLE')
    user_settings_df = add_user_settings(user_settings_df,'Aneesh',        '39360',  8,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Aryan',         '88888888', 9, 4,'thisthing.png'   ,'BLUE') #16878794 old
    user_settings_df = add_user_settings(user_settings_df,'Austin',        '14781', 15,-1,'Default.png'     ,'GOLD')
    user_settings_df = add_user_settings(user_settings_df,'Caitlyn',       '39387',  16,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Emma',          '24966', 17,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Evan',          '14764', 18, 2,'EvaninFTCBox.png','RED')
    user_settings_df = add_user_settings(user_settings_df,'Hisham',        '39371',  19,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Jared',         '39339',  25,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Juliet',        '39341',  26,-1,'Default.png',    'PINK')
    user_settings_df = add_user_settings(user_settings_df,'Keita',         '14724', 27,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Liam',          '14701', 28,-1,'Default.png'     ,'BLUE')
    user_settings_df = add_user_settings(user_settings_df,'Luke',          '88888888', 29,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Madison',       '39301',  35,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Manav',         '39315',  36,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Martin',        '39321', 37, 6,'Chargedup.png'   ,'CYAN')
    user_settings_df = add_user_settings(user_settings_df,'Naaisha',       '39352',  38,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Nathan',        '14742', 39,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Rebagrace',     '14713', 45,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Roshan',        '44806', 46,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Ryan',          '14791', 47,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Sreeya',        '39362',  48,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Tejas',         '39390',  49,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Vikas',         '14719', 55,-1,'Default.png'     ,'GREEN')
    user_settings_df = add_user_settings(user_settings_df,'Xavier',        '39303',  56,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Kent',          '39325',  57,-1,'Default.png',    'RED')
    user_settings_df = add_user_settings(user_settings_df,'Adarsh',        '39361',  58,-1,'Default.png',    'RED')
    return user_settings_df


#Displays text on the screen
def display_text(screen, text, position=(0, 0), size=36, color=(255, 255, 255), font_name=None):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def display_centered_text(screen, message, position=(0, 0), font_size=36, color=(255, 255, 255), font_name=None):
    font = pygame.font.Font(font_name, font_size)  # Use None for pygame's default font
    text_surface = font.render(message, True, color)
    
    # Compute the top-left corner of the text to ensure (x, y) is at the center
    text_rect = text_surface.get_rect(center=position)
    
    screen.blit(text_surface, text_rect)

def Set_MPIB_Status_Global(users_df,user_settings_df):
    #print("MPIB Status at start: ", str(self.MPIB_Status))
    tempstr = ""
    exclude = []
    mpib_slot = []
    exclude.append("00000000")
    #print(str(exclude))
    for i in range(len(users_df),-1,-1): #Iterate backwards through scheckin DB
        if(i > 0 and i < len(users_df) - 1):
            flagged = False
            for j in exclude:
                if not(str(users_df.loc[i,'ID']) == str(j)):
                    temp_ID = str(users_df.loc[i,'ID'])

                    temploc = ""
                    tempcolor = ""
                    for l in range(len(user_settings_df)):#Looks through settings DB to match the ID and find the MPIB ID
                        if (str(user_settings_df.loc[l,'ID']) == str(users_df.loc[i,'ID']) and not(flagged)):
                            temploc = user_settings_df.loc[l,'MPIB']
                            mpib_slot.append(temploc)
                            for k in exclude:
                                if (str(users_df.loc[i,'ID']) == str(k)):
                                    break
                            else:
                                exclude.append(str(users_df.loc[i,'ID']))
                                flagged = True
                                #print("Exclude list: ", str(exclude))
                                if (users_df.loc[i,'CIOO'] == True): #Check if in and assign color
                                    #print("User ", str(self.users_df.loc[i,'ID']), " checked in")
                                    #print("1CIOO = ", str(self.users_df.loc[i,'CIOO']))
                                    tempcolor = "GREEN"
                                elif (users_df.loc[i,'CIOO'] == False): #Check if out and assign color
                                    #print("User ", str(self.users_df.loc[i,'ID']), " checked out")
                                    #print("2CIOO = ", str(self.users_df.loc[i,'CIOO']))
                                    tempcolor = "RED"
                                tempstr = tempstr + str(temploc) + "," + str(tempcolor) + "|"
                            break
    #for count in range(80):
    #    for r in mpib_slot:

    MPIB_Status = str(tempstr)

    if (str(MPIB_Status) == ""):
        MPIB_Status = "0"
    return MPIB_Status


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
        display_centered_text(screen,'Checked in at: ' + datetime.datetime.now().strftime("%I:%M:%S %p"),(400,200),72,WHITE,None)
    else:
        display_centered_text(screen,'Checked out at: ' + datetime.datetime.now().strftime("%I:%M:%S %p"),(400,200),72,RED,None)
    pygame.display.flip()    
    pass

def CheckEveryoneOut(users_df):
    numcolumns = users_df.shape[0] - 1
    print("users_df.shape[1]" + str(users_df.shape[0]))
    id_list = []
    id_list.append("00000000")
    print("ID List in the beginning: " + str(id_list))
    exclude_list = []
    exclude_list.append("00000000")
    exclude = 0
    clean_up = 1
    if (clean_up == 1):
        for i in range(numcolumns, -1, -1):
            print("In loop: " + str(i) + " ID: " + str(users_df.loc[i,'ID']))
            exclude = 0
            if (users_df.loc[i,'CIOO'] == True):
                if (len(id_list) > 0):
                    for j in range(len(id_list)):
                        if (i == 85):
                            print("User DF ID: " + str(users_df.loc[i,'ID']) + " VS id_list: " + str(id_list[j]))
                        if (str(users_df.loc[i,'ID']) == str(id_list[j])):
                            print("Broke out because self.users_df.loc[i,'ID'] == id_list[j]")
                            break
                    else:
                        print("No breakout, checking exclude list")
                        if (len(exclude_list) > 0):
                            for e in range(len(exclude_list)):
                                if (i == 85):
                                    print("User DF ID: " + str(users_df.loc[i,'ID']) + " VS exclude_list: " + str(exclude_list[e]))
                                if (str(users_df.loc[i,'ID']) == str(exclude_list[e])):
                                    print("On excluded list")
                                    exclude = 1
                        if (exclude == 0):
                            id_list.append(str(users_df.loc[i,'ID']))
                            print("Appended: self.users_df.loc[i,'ID'] : " + str(users_df.loc[i,'ID']) + " to the id_list")
            elif (users_df.loc[i,'CIOO'] == False):
                if (len(id_list) > 0):
                    in_id_list = 0
                    for j in range(len(id_list)):
                        if (str(users_df.loc[i,'ID']) == str(id_list[j])):
                            in_id_list = 1
                            break
                    if(in_id_list == 0):
                        exclude_list.append(str(users_df.loc[i,'ID']))
        print("len(id_list) :" + str(len(id_list)))
        if (len(id_list) > 0):
            for i in range(len(id_list)):
                if(str(id_list[i]) != "00000000"):
                    name = ""
                    for q in range(user_settings_df.shape[0]):
                        if(str(user_settings_df.loc[q,'ID']) == str(id_list[i])):
                            name = user_settings_df.loc[q,'Name']       
                    users_df = users_df.append({'ID': id_list[i], 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"),'CIOO': False}, ignore_index=True)
                    print ('ID: ', str(id_list[i]), ' , CIOT: ', str(datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y")) , ' CIOO: OUT')
        clean_up = 0
        Just_Save('checkins2.csv')

#Function to process any serial data we receive.  Should handle bad data/incomplete data
def Process_Serial_Data(ser_data,user_settings_df, screen):
    if (ser_data):
        for i in range(len(user_settings_df)):
            if(str(ser_data) == str(user_settings_df.loc[i,'ID'])):
                print('Got to before check in screen')
                #post a new pygame event.  Name first, then any parameters you want to pass in
                PlaySound('Audio/Success.mp3')
                pygame.event.post(pygame.event.Event(ID_GET, ID_NUM=ser_data,TIME_STAMP=datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y")))
                break
        else:
            
            if(str(ser_data) == ('14758')):
                
                pass
            elif (str(ser_data) == ('16878687')):
                pass
            else:
                PlaySound('Audio/Fail.mp3')
                pass



def Add_Checkinorout(screen, checkin_df,user_settings_df, ID):
    global update_MPIB
    inorout = False
    for i in range(len(checkin_df)-1, -1, -1):
        #print (str(checkin_df.at[i, 'ID']) + ' == ' + str(ID))
        if (str(checkin_df.at[i, 'ID']) == str(ID)):
            if checkin_df.at[i, 'CIOO'] == True:
                tempname = "Error"
                for j in range(len(user_settings_df)):
                    if(str(ID) == str(user_settings_df.loc[j,'ID'])):
                        tempname = user_settings_df.loc[j,'Name']
                        update_MPIB = str(user_settings_df.loc[j,'MPIB']) + ",RED"
                        break
                inorout = False
                print(tempname, ' has checked out')
                new_data = pd.DataFrame([{'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"), 'CIOO': False}])
                CheckInOutScreen(screen, inorout, tempname,"","","","","")
            elif(checkin_df.at[i, 'CIOO'] == False):
                tempname = "Error"
                for j in range(len(user_settings_df)):
                    if(str(ID) == str(user_settings_df.loc[j,'ID'])):
                        tempname = user_settings_df.loc[j,'Name']
                        update_MPIB = str(user_settings_df.loc[j,'MPIB']) + ",GREEN"
                        break
                inorout = True
                print(tempname, ' has checked in')
                new_data = pd.DataFrame([{'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"), 'CIOO': True}])
                CheckInOutScreen(screen, inorout, tempname, "", "", "", "","")
            checkin_df = pd.concat([checkin_df, new_data], ignore_index=True)
            break
    else:
        tempname = "Error"
        for j in range(len(user_settings_df)):
            if(str(ID) == str(user_settings_df.loc[j,'ID'])):
                tempname = user_settings_df.loc[j,'Name']
                update_MPIB = str(user_settings_df.loc[j,'MPIB']) + ",GREEN"
                break
        inorout = True
        print(tempname, ' has checked in fallthrough')
        new_data = pd.DataFrame([{'ID': ID, 'CIOT': datetime.datetime.now().strftime("%I:%M:%S %p %B %d, %Y"), 'CIOO': True}])
        checkin_df = pd.concat([checkin_df, new_data], ignore_index=True)
        CheckInOutScreen(screen, inorout, tempname,"","","","","")

    Just_Save(checkin_df,'checkins2.csv')
    ser.flush()
    return checkin_df

def start_server(host='192.168.214.223', port=8080):
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

def handle_client(conn):
    global update_MPIB
    global refresh_MPIB
    while True:
        data = conn.recv(1024)
        if not data:
            break
        #print(f"Received data: {data.decode('utf-8')}")
        rdata = data
        #print("radta: ",str(rdata))
        if rdata == b"update":
            if (update_MPIB == ""):
                response = "No"
            else:
                response=update_MPIB      
                print('Sent: ', str(response))          
            conn.send(response.encode('utf-8'))
            update_MPIB = "No"
            #print("Received update")
        elif(rdata == b"refresh"):
            pass
            print("Received refresh")
            print("MPIB_Status: ", refresh_MPIB)
            if (refresh_MPIB == ""):
                response = "No"
            else:
                response=refresh_MPIB
            print("Response: ", str(response))
            conn.send(response.encode('utf-8'))
            update_MPIB = ""
    conn.close()

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
    pygame.mixer.pre_init(frequency=48000, buffer=2048)
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
    idle_flag = False
    splashimage = pygame.image.load("Images/FIRSTNewton2Logo-Instructions.png")

    # Start the server in a new thread
    #server_thread = threading.Thread(target=start_server)
    #server_thread.start()

    while running:
        #Check Serial connection
        #if (CheckPlatform() == 1):
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
        if (elapsed_time > 5 and elapsed_time < 5.05):
            #refresh_MPIB = Set_MPIB_Status_Global(checkin_df,user_settings_df)
            print(str(refresh_MPIB))
            screen.fill((0,0,0))
            screen.blit(splashimage, (0, 0))
            pygame.display.flip()

        for event in pygame.event.get():           
            if(event.type == ID_GET):
                checkin_df = Add_Checkinorout(screen, checkin_df,user_settings_df,event.ID_NUM)
                idle = time.perf_counter()
            elif(event.type == pygame.QUIT):
                running = False
                #
                pygame.quit()
                sys.exit()
        clock.tick(60)




        