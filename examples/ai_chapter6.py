from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import keyboard # keyboard==0.13.4
import time

PingPongThreadInstance = PingPongThread(number=2) # n개 로봇 연결
PingPongThreadInstance.start() # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림
cube_ID = 1

PingPongThreadInstance.webcam_open()

bill = PingPongThreadInstance.ImageClass("bill", "chapter6/bill")
fake = PingPongThreadInstance.ImageClass("fake", "chapter6/fake")
model = PingPongThreadInstance.train_classes("chapter6/bill_model.json", 1, 2, bill, fake)

print("여기에 지폐를 인식시키면")
time.sleep(1)
print("위조지폐 여부를 알 수 있대")
time.sleep(1)
while True:
    if keyboard.is_pressed(" "):
        break
    else:
        time.sleep(0.01)
time.sleep(4)
print("재미있겠다~ 빨리 해보자!")
time.sleep(2)

PingPongThreadInstance.tts_ko("지폐를 인식시켜 주세요", True)
time.sleep(2)

PingPongThreadInstance.webcam_open()
frames_predictor = PingPongThreadInstance.FramesPredictor(model=model, timer_sec=3)
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
    if max_class == "bill" and accum_prediction[max_class] > 0.9:
        PingPongThreadInstance.tts_ko("우리나라 지폐", True)
        angle = 50/360
        PingPongThreadInstance.run_motor_step([1, 2], 15, [-angle, angle])
        time.sleep(angle/15*60)
        PingPongThreadInstance.run_motor_step([1, 2], 15, [angle, -angle])
        time.sleep(angle/15*60)
        break
    elif max_class == "fake" and accum_prediction[max_class] > 0.9:
        PingPongThreadInstance.play_music(1, ["mi", "do", "mi", "do"], ["half"]*4)
        PingPongThreadInstance.tts_ko("위조 지폐", True)
        PingPongThreadInstance.tts_ko("위조 지폐", True)
        angle = 45/360
        PingPongThreadInstance.run_motor_step([1, 2], 15, [angle, angle])
        time.sleep(angle/15*60)
        PingPongThreadInstance.run_motor_step([1, 2], 15, [-angle, -angle])
        time.sleep(angle/15*60)
        PingPongThreadInstance.run_motor_step([1, 2], 15, [-angle, -angle])
        time.sleep(angle/15*60)
        PingPongThreadInstance.run_motor_step([1, 2], 15, [angle, angle])
        time.sleep(angle/15*60)
        break
    else:
        continue
    

PingPongThreadInstance.webcam_close()
PingPongThreadInstance.destroy_webcam_window(window="Get_frame")
PingPongThreadInstance.end()