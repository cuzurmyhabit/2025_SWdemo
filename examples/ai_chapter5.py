from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import keyboard # keyboard==0.13.4
import time

PingPongThreadInstance = PingPongThread(number=2) # n개 로봇 연결
PingPongThreadInstance.start() # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림
cube_ID = 1

PingPongThreadInstance.webcam_open()

general = PingPongThreadInstance.ImageClass("general", "chapter5/general")
recycle = PingPongThreadInstance.ImageClass("recycle", "chapter5/recycle")
model = PingPongThreadInstance.train_classes("chapter5/waste_model.json", 1, 2, general, recycle)

PingPongThreadInstance.receive_sensor_data(cube_ID, method="periodic", period=0.5)
proxy_default = PingPongThreadInstance.get_default_proxy(cube_ID)

while True:
    # 근접 센서 변화량.
    proxy_diff = abs(PingPongThreadInstance.get_current_proxy(cube_ID) - proxy_default)
    # 근접 센서 변화량이 10을 넘으면 3초 쉬고 마스크 검사. 
    if 10 < proxy_diff:
        text = "안녕하세요? 생활에서 중요한 재활용 분리수거. 제가 도와드릴게요! 이미지를 보여주세요."
        print(text)
        break
    else:
        print("장애물이 감지되지 않았어요.")
        time.sleep(0.1)
        # 출력 비우기.
        PingPongThreadInstance.clear_output()

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
    if max_class == "general" and accum_prediction[max_class] > 0.9:
        text = "일반쓰레기"
        PingPongThreadInstance.tts_ko(text)
        PingPongThreadInstance.run_motor_step(cube_ID, 15, -0.25)
        time.sleep(2)
        PingPongThreadInstance.run_motor_step(cube_ID, 15, 0.25)
    elif max_class == "recycle" and accum_prediction[max_class] > 0.9:
        text = "재활용 쓰레기"
        PingPongThreadInstance.tts_ko(text)
        PingPongThreadInstance.run_motor_step(cube_ID, 15, 0.25)
        time.sleep(2)
        PingPongThreadInstance.run_motor_step(cube_ID, 15, -0.25)
    else:
        continue
    text = "더 버릴 쓰레기가 있으신가요? (있으면 1 아니면 0): "
    PingPongThreadInstance.tts_ko(text)
    x = input(text)
    if x == "1":
        text = "이미지를 보여주세요!"
        PingPongThreadInstance.tts_ko(text)
        print(text)
        frames_predictor.clear_accum()
        continue
    else:
        text = "분리수거를 생활화합시다!"
        PingPongThreadInstance.tts_ko(text)
        print(text)
        break

PingPongThreadInstance.webcam_close()
PingPongThreadInstance.destroy_webcam_window(window="Get_frame")
PingPongThreadInstance.end()