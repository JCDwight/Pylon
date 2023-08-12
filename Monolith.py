import platform as plat
import pygame
import sys
import time

pygame.init()
pygame.mixer.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 300

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple UI in Pygame')
clock = pygame.time.Clock()


# Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('arial', 20)
        text = font.render(self.text, True, BLACK)
        win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

button = Button(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 - 20, 100, 40, "Click Me!")
bg_color = WHITE

def CheckPlatform():
    #Checks the platform the program is running on.  Linux = 1, Windows = 2, everything else is 3
    if (plat.platform()[0] == "L" or plat.platform()[0] == "l"):
        return 1
    elif (plat.platform()[0] == "W" or plat.platform()[0] == "w"):
        return 2
    else:
        return 3
    
def PlaySound(sound):
    temp_sound = pygame.mixer.Sound(sound)
    temp_sound.play()

if __name__ == '__main__':
    if (CheckPlatform() == 2):
        pass
    else:
        running = True
        while running:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.is_over(pos):
                        PlaySound('coins.wav')
                        bg_color = RED if bg_color == WHITE else WHITE

            screen.fill(bg_color)
            button.draw(screen, GREEN)
            pygame.display.flip()

            clock.tick(60)




        