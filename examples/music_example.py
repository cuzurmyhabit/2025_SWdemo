from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import time

PingPongThreadInstance = PingPongThread(number=1)
PingPongThreadInstance.start()
PingPongThreadInstance.wait_until_full_connect()

PingPongThreadInstance.play_music(1, ["do", "re", "mi", "fa", "sol", "la", "ti"], ["whole"]*7)


while True:
    #print("Thread working... (5 sec.)")
    time.sleep(10)