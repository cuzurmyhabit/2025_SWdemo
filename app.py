from pingpongthread import PingPongThread
import time
import keyboard

PingPong = PingPongThread(number=2, group_id=40)
PingPong.start()
PingPong.wait_until_full_connect()

while not keyboard.is_pressed("esc"):
    if keyboard.is_pressed("up"):
        PingPong.run_motor([1,2], [-15,15]) 
    
    if keyboard.is_pressed("down"):
        PingPong.run_motor([1,2], [15,-15])
        
    if keyboard.is_pressed("right"):
        PingPong.run_motor([1,2], [-7,-7]) 

    if keyboard.is_pressed("left"):
        PingPong.run_motor([1,2], [7,7])
        
    elif keyboard.is_pressed("space"):
        PingPong.run_motor([1,2], "stop")
        
PingPong.end()