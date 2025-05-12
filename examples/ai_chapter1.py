from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import keyboard # keyboard==0.13.4
import time

cube_ID = 1

PingPongThreadInstance = PingPongThread(number=cube_ID) # n개 로봇 연결
PingPongThreadInstance.start() # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

'''
### 01 근접 센서 명령어 블록
# 근접 센서 데이터를 받기
PingPongThreadInstance.receive_sensor_data(cube_ID, method="periodic", period=0.5)
while not keyboard.is_pressed("q"): # q가 눌리기 전까지 반복
    # 현재 근접 센서값 출력
    print(PingPongThreadInstance.get_current_proxy(cube_ID))
    # 0.5초 기다리기
    time.sleep(0.5)
PingPongThreadInstance.stop_sensor_data(cube_ID) 

### 02 스탭 모터 명령어 블록
# 모터를 반시계 방향으로 90도 회전하기
angle = 90/360
PingPongThreadInstance.run_motor_step(1, 15, -angle)
time.sleep(angle/15*60)
# 4초 기다리기
time.sleep(4)
# 모터를 시계방향으로 90도 회전하기
PingPongThreadInstance.run_motor_step(1, 15, angle)
time.sleep(angle/15*60)

### 03 버튼 명령어 블록
# 버튼 데이터를 받기
PingPongThreadInstance.receive_sensor_data(cube_ID, method="periodic", period=0.5)
while not keyboard.is_pressed("q"): # q가 눌리기 전까지 반복
    # 버튼이 눌리면 "안녕!"이라고 말하기
    if PingPongThreadInstance.get_current_button(cube_ID) == 1:
        print("안녕!")
        # 4초 기다리기
        time.sleep(4)
        break
    # 0.5초 기다리기
    time.sleep(0.5)
PingPongThreadInstance.stop_sensor_data(cube_ID) 
'''

### 04 기울기 센서 명령어 블록
# 센서 데이터를 받기
PingPongThreadInstance.receive_sensor_data(cube_ID, method="periodic", period=0.1)
while not keyboard.is_pressed("q"): # q가 눌리기 전까지 반복
    gyro_value = PingPongThreadInstance.get_current_gyro(cube_ID)
    # 네모 방향으로 빠르게 움직이면 "네모 방향으로 회전하였습니다!"를 출력
    if gyro_value[0] < -90 and abs(gyro_value[1]) < 50 and abs(gyro_value[2]) < 50:
        print("네모 방향으로 회전하였습니다!")
        break
    # 0.1초 기다리기
    time.sleep(0.1)
PingPongThreadInstance.stop_sensor_data(cube_ID) 

PingPongThreadInstance.end()