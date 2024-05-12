import threading
import time
import pyautogui
import pygame

def mouseloop(event):
    
    pyautogui.FAILSAFE = False

    while True:
        pyautogui.moveTo(x = 0, y = 0)
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        if event.is_set():
            break


def main():
    count = 0
    step = 1

    event = threading.Event()
    threadmouse = threading.Thread(target=mouseloop, args=(event,))
    threadmouse.start()
    for _ in range(10):
        time.sleep(step)
        count += step
        print(count, " sec normal")
    event.set()
    threadmouse.join()

if __name__ == "__main__":
    main()