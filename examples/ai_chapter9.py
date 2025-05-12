from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import time
import keyboard
import random

PingPongThreadInstance = PingPongThread(number=1) # 2개 로봇 연결
PingPongThreadInstance.start()
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

cube_ID = 1

PingPongThreadInstance.webcam_open()
#PingPongThreadInstance.webcam_take_snapshots("chapter9/rock")
#PingPongThreadInstance.webcam_take_snapshots("chapter9/paper")
#PingPongThreadInstance.webcam_take_snapshots("chapter9/scissors")

rock = PingPongThreadInstance.ImageClass("rock", "chapter9rock")
paper = PingPongThreadInstance.ImageClass("paper", "chapter9/paper")
scissors = PingPongThreadInstance.ImageClass("scissors", "chapter9/scissors")
model = PingPongThreadInstance.train_classes("chapter9/rps_model.json", 10, 2,  rock, paper, scissors)

print("스페이스 키를 누르면 가위바위보 게임을 시작합니다!")
time.sleep(4)
while True:
    if keyboard.is_pressed(" "):
        break
    else:
        time.sleep(0.1)

print("가위바위보!")
x = random.randint(0, 2)
angle = [60/360, 180/360, 240/360][x] # rock, scissors, paper

PingPongThreadInstance.webcam_open()
frames_predictor = PingPongThreadInstance.FramesPredictor(model=model, timer_sec=3)
while True:
    frame = PingPongThreadInstance.webcam_get_frame(window="Get_frame")
    frames_prediction = frames_predictor.image_predict_and_accum(frame)
    print(frames_prediction)
    accum_prediction = frames_predictor.accum_predict()
    if accum_prediction == None:
        max_class = None
        continue
    else:
        print("accum_prediction:", accum_prediction)
        max_class = max(accum_prediction, key=accum_prediction.get)
    if max_class == "rock" and accum_prediction[max_class] > 0.9:
        print("인식된 손 모양:", max_class)
        if x == 0:
            print("바위!")
            print("비겼다...")
        elif x == 1:
            print("가위!")
            print("졌다 ㅠㅠ")
        else:
            print("보!")
            print("이겼다~!")
        time.sleep(2)
        PingPongThreadInstance.run_motor_step(cube_ID, 15, angle)
        break
    elif max_class == "paper" and accum_prediction[max_class] > 0.9:
        print("인식된 손 모양:", max_class)
        if x == 0:
            print("바위!")
            print("졌다 ㅠㅠ")
        elif x == 1:
            print("가위!")
            print("이겼다~!")
        else:
            print("보!")
            print("비겼다...")
        time.sleep(2)
        PingPongThreadInstance.run_motor_step(cube_ID, 15, angle)
        break
    elif max_class == "scissors" and accum_prediction[max_class] > 0.9:
        print("인식된 손 모양:", max_class)
        if x == 0:
            print("바위!")
            print("이겼다~!")
        elif x == 1:
            print("가위!")
            print("비겼다...")
        else:
            print("보!")
            print("졌다 ㅠㅠ")
        time.sleep(2)
        PingPongThreadInstance.run_motor_step(cube_ID, 15, angle)
        break
    else:
        continue