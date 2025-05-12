from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import keyboard 
import time

group_id = 4
PingPongThreadInstance = PingPongThread(number=1, group_id=group_id) # n개 로봇 연결
PingPongThreadInstance.start(group_id=group_id) # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

PingPongThreadInstance.end() # 쓰레드 종료
del PingPongThreadInstance

PingPongThreadInstance = PingPongThread(number=2, group_id=group_id) # n개 로봇 연결
PingPongThreadInstance.start(group_id=group_id) # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

time.sleep(5)
PingPongThreadInstance.end() # 쓰레드 종료