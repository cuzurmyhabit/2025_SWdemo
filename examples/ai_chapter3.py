# ai_chapter3.py

from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import keyboard
import time
import datetime

PingPongThreadInstance = PingPongThread(number=2) # 2개 로봇 연결
PingPongThreadInstance.start()
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

text = '스페이스 키를 누른 뒤 "지금 몇시야?"라고 말해보세요!'
PingPongThreadInstance.tts_ko(text)
print(text)
while True:
    if keyboard.is_pressed(" "):
        print("마이크를 인식하는 중입니다.")
        result = PingPongThreadInstance.voice_recognize_ko()
        print("결과:", result)
        result = result.replace(" ", "")
        if "지금몇시야" not in result:
            text = "스페이스 키를 누르고 다시 말씀해주세요!"
            PingPongThreadInstance.tts_ko(text)
            print(text)
        else:
            now = datetime.datetime.now()
            now_hour = now.hour
            now_minute = now.minute
            text = "{} 시 {} 분입니다.".format(now_hour, now_minute)
            PingPongThreadInstance.tts_ko(text)
            print(text)

            hour_cycle = (now_hour%12)/12
            minute_cycle = now_minute/60
            PingPongThreadInstance.run_motor_step(cube_ID_list=[1, 2], speed_list=15, step_list=[hour_cycle, minute_cycle])
            time.sleep(3)
    else:
        time.sleep(0.1)


PingPongThreadInstance.end()