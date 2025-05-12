from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import keyboard # keyboard==0.13.4
import time

# https://velog.io/@mactto3487/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-OpenCV-%EC%9E%90%EB%8F%99%EC%B0%A8-%EB%B2%88%ED%98%B8%ED%8C%90-%EC%9D%B8%EC%8B%9D

PingPongThreadInstance = PingPongThread(number=1) # n개 로봇 연결
PingPongThreadInstance.start() # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림
cube_ID = 1

PingPongThreadInstance.webcam_open()

registered = PingPongThreadInstance.ImageClass("registered", "chapter10/registered")
unregistered = PingPongThreadInstance.ImageClass("unregistered", "chapter10/unregistered")
model = PingPongThreadInstance.train_classes("chapter10/license_place_model.json", 10, 2, registered, unregistered)

print("안녕하세요? 저는 핑퐁주차로봇입니다.")
time.sleep(2)
print("번호가 등록된 차량만 등록하실 수 있습니다. 차량번호를 인식하겠습니다.")
time.sleep(2)

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
    if max_class == "registered" and accum_prediction[max_class] > 0.9:
        print("등록된 차량입니다. 주차바가 자동으로 올라갑니다.")
        time.sleep(2)
        angle = 90/360
        PingPongThreadInstance.run_motor_step(1, 15, angle)
        time.sleep(angle/15*60+2)
        PingPongThreadInstance.run_motor_step(1, 15, -angle)
        time.sleep(angle/15*60+2)
        print("진입하십시오! 주차장에 오신 것을 환영합니다.")
        time.sleep(2)
        break
    elif max_class == "unregistered" and accum_prediction[max_class] > 0.9:
        PingPongThreadInstance.play_music(1, ["do"], ["whole"])
        print("죄송합니다. 이 번호는 등록되지 않은 차량이오니 등록 후 주차장을 이용하여 주시기 부탁드립니다.")
        break
    else:
        continue
    
PingPongThreadInstance.webcam_close()
PingPongThreadInstance.destroy_webcam_window(window="Get_frame")
PingPongThreadInstance.end()
del PingPongThreadInstance



PingPongThreadInstance = PingPongThread(number=2) # n개 로봇 연결
PingPongThreadInstance.start() # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

angle = 90/360
while True:
    if keyboard.is_pressed("up"):
        PingPongThreadInstance.run_motor_step([1, 2], 15, [-angle, angle])
        time.sleep(angle/15*60)
    elif keyboard.is_pressed("down"):
        PingPongThreadInstance.run_motor_step([1, 2], 15, [angle, -angle])
        time.sleep(angle/15*60)
    elif keyboard.is_pressed("left"):
        PingPongThreadInstance.run_motor_step([1, 2], 15, [angle, angle])
        time.sleep(angle/15*60)
    elif keyboard.is_pressed("right"):
        PingPongThreadInstance.run_motor_step([1, 2], 15, [-angle, -angle])
        time.sleep(angle/15*60)
    elif keyboard.is_pressed("q"):
        break
    else:
        time.sleep(0.1)

PingPongThreadInstance.end()
del PingPongThreadInstance