from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import time
import keyboard

PingPongThreadInstance = PingPongThread(number=1, tensorflow_no_warnings=True) # 2개 로봇 연결
PingPongThreadInstance.start()
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

cube_ID = 1

PingPongThreadInstance.webcam_open()
PingPongThreadInstance.webcam_take_snapshots("chapter4/good")
PingPongThreadInstance.webcam_take_snapshots("chapter4/bad")

good = PingPongThreadInstance.ImageClass("good", "chapter4/good")
bad = PingPongThreadInstance.ImageClass("bad", "chapter4/bad")
model = PingPongThreadInstance.train_classes("chapter4/gb_model.json", 10, 2, good, bad)

print("스페이스 키를 누르고 당신의 감정을 표현해 보세요!")
time.sleep(4)
while True:
    if keyboard.is_pressed(" "):
        break
    else:
        time.sleep(0.01)

now = 1
flag = 1
frames_predictor = PingPongThreadInstance.FramesPredictor(model=model, timer_sec=3)
while True:
    if keyboard.is_pressed("q"):
        break

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
    
    if max_class == "good" and accum_prediction[max_class] > 0.9:
        now = 1  
    elif max_class == "bad" and accum_prediction[max_class] > 0.9:
        now = 2
    else:
        continue

    if now == flag:
        pass
    else:
        angle = 180/360
        PingPongThreadInstance.run_motor_step(cube_ID, 15, angle)
        time.sleep(angle/15*60)
        flag = now

# 웹캠 닫기.
PingPongThreadInstance.webcam_close()
# 로봇 제어 쓰레드 종료.
PingPongThreadInstance.end()
    
