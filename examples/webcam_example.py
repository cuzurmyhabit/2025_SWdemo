from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import keyboard # keyboard==0.13.4

PingPongThreadInstance = PingPongThread(number=1) # n개 로봇 연결
PingPongThreadInstance.start() # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

PingPongThreadInstance.webcam_open()
PingPongThreadInstance.webcam_take_snapshots("week2/no_mask")
PingPongThreadInstance.webcam_take_snapshots("week2/with_mask")