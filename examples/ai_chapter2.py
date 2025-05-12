from example_base import GetParentPath # 상위 폴더 경로 가져오기
from pingpongthread import PingPongThread
import time

cube_ID = 1

PingPongThreadInstance = PingPongThread(number=cube_ID) # n개 로봇 연결
PingPongThreadInstance.start() # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

PingPongThreadInstance.webcam_open()
PingPongThreadInstance.webcam_take_snapshots("chapter2/no_mask")
PingPongThreadInstance.webcam_take_snapshots("chapter2/with_mask")

no_mask = PingPongThreadInstance.ImageClass("no_mask", "chapter2/no_mask")
with_mask = PingPongThreadInstance.ImageClass("with_mask", "chapter2/with_mask")
model = PingPongThreadInstance.train_classes("chapter2/mask_model.json", 5, 1, no_mask, with_mask)

PingPongThreadInstance.receive_sensor_data(cube_ID, method="periodic", period=0.5)
proxy_default = PingPongThreadInstance.get_default_proxy(cube_ID)

mask_examine = False
while True:
    proxy_diff = abs(PingPongThreadInstance.get_current_proxy(cube_ID) - proxy_default)
    print("proxy_diff", proxy_diff)
    if 10 < proxy_diff:
        mask_examine = True
        print("마스크를 검사할게요~.")
        break
    else:
        time.sleep(0.1)

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
    if max_class == "with_mask" and accum_prediction[max_class] > 0.9:
        print("마스크를 잘 착용하고 왔네요~. 등교를 환영합니다!")
        PingPongThreadInstance.run_motor_step(cube_ID, 15, -0.25)
        time.sleep(4)
        PingPongThreadInstance.run_motor_step(cube_ID, 15, 0.25)
        break
    else:
        print("이런… 마스크를 깜빡 했나보군요… 마스크를 착용하고 등교해주세요!")
        frames_predictor.clear_accum()

PingPongThreadInstance.stop_sensor_data(cube_ID) 
PingPongThreadInstance.webcam_close()
PingPongThreadInstance.destroy_webcam_window(window="Get_frame")
PingPongThreadInstance.end()