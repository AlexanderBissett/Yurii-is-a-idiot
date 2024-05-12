from clinst import CustomCounter
import pygame
from pygame.locals import FULLSCREEN
import time
import threading
import ctypes

def game(eventino):
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    address = r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.22621.0\x86'

    bg = []
    for i in range (14):
        filename = fr'{address}\{i}.jpg'
        bgfile = pygame.image.load(filename)
        bg.append(bgfile)

    dark_blue = 0, 74, 173

    screen = pygame.display.set_mode(screensize, FULLSCREEN)
    pygame.mouse.set_visible(0)
    
    while not eventino.is_set():
        idx = cc.cnt
        screen.fill(dark_blue)
        screen.blit(bg[idx], (0, 0))
        pygame.display.update()


cc = CustomCounter(0)
event = threading.Event()
thread = threading.Thread(target=game, args=(event,))
thread.start()
for c in range (14):
    cc.cnt = c
    time.sleep(2)

event.set()
thread.join()
