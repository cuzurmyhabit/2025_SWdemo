from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import time

PingPongThreadInstance = PingPongThread(number=2) # 2개 로봇 연결
PingPongThreadInstance.start()
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

PingPongThreadInstance.tts_ko("안전벨트를 매주세요. 320 미터 직진입니다.", True)
time.sleep(2)
angle = 320/360
PingPongThreadInstance.run_motor_step([1, 2], 15, [-angle, angle])
time.sleep(angle/15*60)

PingPongThreadInstance.tts_ko("2초간 멈추세요.", True)
time.sleep(2)

PingPongThreadInstance.tts_ko("200미터 앞 우회전입니다.", True)
time.sleep(1)
angle = 200/360
PingPongThreadInstance.run_motor_step([1, 2], 15, [-angle, angle])
time.sleep(angle/15*60)

PingPongThreadInstance.tts_ko("우회전해 주세요.", True)
time.sleep(1)
angle = 107/360
PingPongThreadInstance.run_motor_step([1, 2], 15, [-angle, -angle])
time.sleep(angle/15*60)

PingPongThreadInstance.tts_ko("500미터 직진입니다.", True)
time.sleep(1)
angle = 500/360
PingPongThreadInstance.run_motor_step([1, 2], 15, [-angle, angle])
time.sleep(angle/15*60)

PingPongThreadInstance.tts_ko("신호등이 있습니다. 잠시 기다려주세요.", True)
time.sleep(5)

PingPongThreadInstance.tts_ko("300미터 전방 목적지가 있습니다.", True)
time.sleep(1)
angle = 300/360
PingPongThreadInstance.run_motor_step([1, 2], 15, [-angle, angle])
time.sleep(angle/15*60)

PingPongThreadInstance.tts_ko("목적지에 도착했습니다.", True)

PingPongThreadInstance.end()