from example_base import GetParentPath
from pingpongthread import PingPongThread
import keyboard # keyboard==0.13.4
import time

PingPongThreadInstance = PingPongThread(number=1) # n개 로봇 연결
PingPongThreadInstance.start() # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

cube_ID = 1 # 큐브 번호

min_proxy = None
while not keyboard.is_pressed("q"): # q가 눌리기 전까지 쓰레드 유지
    while PingPongThreadInstance.play_once_full_connect(): # 연결 되어있는 동안, 한 번만 실행
        PingPongThreadInstance.receive_sensor_data(cube_ID, method="periodic", period=0.1) 
        min_proxy = PingPongThreadInstance.get_min_proxy(cube_ID)
        print(min_proxy)
    print("min:", min_proxy)
    print("curr:", PingPongThreadInstance["sensor_prox"][cube_ID-1])
    time.sleep(0.05)

PingPongThreadInstance.end() # 쓰레드 종료