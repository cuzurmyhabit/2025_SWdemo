from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import keyboard # keyboard==0.13.4
import time

PingPongThreadInstance = PingPongThread(number=2) # n개 로봇 연결
PingPongThreadInstance.start() # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

PingPongThreadInstance.webcam_open()

gangwondo = PingPongThreadInstance.ImageClass("gangwondo", "chapter8/gangwondo")
chungcheongnamdo = PingPongThreadInstance.ImageClass("chungcheongnamdo", "chapter8/chungcheongnamdo")
model = PingPongThreadInstance.train_classes("chapter8/specialties_model.json", 1, 2, gangwondo, chungcheongnamdo)

print("어느 지역의 특산품이지???")
time.sleep(1)
while True:
    if keyboard.is_pressed(" "):
        break
    else:
        time.sleep(0.01)
time.sleep(2)

print("내가 알려주지~")
time.sleep(1)
print("사진을 인식시켜 주면")
time.sleep(1)
print("해당 특산품 지역을 알려줄게")
time.sleep(1)

def scene2():
    PingPongThreadInstance.tts_ko("강원도 특산품입니다.", True)
    angle = 20/360
    PingPongThreadInstance.run_motor_step(1, 15, -angle)
    time.sleep(angle/15*60+1)
    angle = 120/360
    PingPongThreadInstance.run_motor_step(2, 15, -angle)
    time.sleep(angle/15*60+1)
    angle = 120/360
    PingPongThreadInstance.run_motor_step(2, 15, angle)
    time.sleep(angle/15*60+1)
    angle = 20/360
    PingPongThreadInstance.run_motor_step(1, 15, angle)
    time.sleep(angle/15*60)

def scene3():
    PingPongThreadInstance.tts_ko("충청남도 특산품입니다.", True)
    angle = 15/360
    PingPongThreadInstance.run_motor_step(1, 15, angle)
    time.sleep(angle/15*60+1)
    angle = 120/360
    PingPongThreadInstance.run_motor_step(2, 15, -angle)
    time.sleep(angle/15*60+2)
    angle = 120/360
    PingPongThreadInstance.run_motor_step(2, 15, angle)
    time.sleep(angle/15*60+1)
    angle = 15/360
    PingPongThreadInstance.run_motor_step(1, 15, -angle)
    time.sleep(angle/15*60)

PingPongThreadInstance.webcam_open()
frames_predictor = PingPongThreadInstance.FramesPredictor(model=model, timer_sec=5)
frames_predictor.set_knn_k(1)
while True:
    frame = PingPongThreadInstance.webcam_get_frame(window="Get_frame")
    frame_prediction = frames_predictor.image_predict_and_accum(frame)
    print(frame_prediction)
    accum_prediction = frames_predictor.accum_predict()
    if accum_prediction == None:
        max_class = None
        continue
    else:
        print("accum_prediction:", accum_prediction)
        max_class = max(accum_prediction, key=accum_prediction.get)
    if max_class == "gangwondo" and accum_prediction[max_class] > 0.9:
        scene2()
        break
    elif max_class == "chungcheongnamdo" and accum_prediction[max_class] > 0.9:
        scene3()
        break
    else:
        continue
    

PingPongThreadInstance.webcam_close()
PingPongThreadInstance.destroy_webcam_window(window="Get_frame")
PingPongThreadInstance.end()