import time
import keyboard

while True:
    if keyboard.is_pressed("up"):
        print("upup")
    else:
        time.sleep(0.1)