#### Blocking Mouse-movement ####
import threading
import mouse
import time
import pygame
import ctypes
from pygame.locals import FULLSCREEN

global executing
executing = True

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
screen = pygame.display.set_mode(screensize, FULLSCREEN)

def move_mouse():
    #until executing is False, move mouse to (1,0)
    global executing
    
    while executing:
        mouse.move(10000,10000, absolute=True, duration=0)
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

def stop_infinite_mouse_control():
    #stops infinite control of mouse after 10 seconds if program fails to execute
    global executing
    time.sleep(5)
    executing = False

threading.Thread(target=move_mouse).start()

threading.Thread(target=stop_infinite_mouse_control).start()
#^failsafe^
