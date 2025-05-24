from pingpong import PingPongThread
import time
import keyboard

pingpong = PingPongThread(number=1, group_id=23)
pingpong.start()
pingpong.wait_until_full_connect()

cube_ID = 1

pingpong.receive_sensor_data(cube_ID=cube_ID, method="periodic", period = 0.5)

try:
    while True:
        temp = pingpong.get_current_temperature(cube_ID)
        print(f"Current temperature: {temp}°C")
        print(pingpong.get_current_proxy(1), end=",")  
        
        if temp >= 21:
            # 모터를 시계 방향(1)으로 속도 100으로 회전
           pingpong.run_motor (1, 30)

        elif  pingpong.get_current_proxy(1) > 150 :
            pingpong.stop_motor(1)

        elif temp <= 20:
            # 온도가 26 이하일 경우 모터 정지
            pingpong.stop_motor(1)

        time.sleep(0.5)

finally:
    # 센서 데이터 수신 중지 및 종료 처리
    pingpong.stop_sensor_data(cube_ID)
    # 모터도 반드시 정지시켜야 함
    pingpong.set_motor_control(cube_ID=cube_ID, motor_id=1, direction=1, speed=0)
    pingpong.end()