import keyboard
import time

#blocks all keys of keyboard
for i in range(200):
    keyboard.block_key(i)
time.sleep (10)