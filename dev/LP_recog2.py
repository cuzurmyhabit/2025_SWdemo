# https://maxtime1004.tistory.com/37
# https://github.com/dpwls64/tesseract_project
# https://joyhong.tistory.com/79
# https://velog.io/@mactto3487/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-OpenCV-%EC%9E%90%EB%8F%99%EC%B0%A8-%EB%B2%88%ED%98%B8%ED%8C%90-%EC%9D%B8%EC%8B%9D


import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

plt.style.use('dark_background')
 
img_ori = cv2.imread('Z13an9857X.jpg')

rgb = cv2.cvtColor(img_ori, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

text = pytesseract.image_to_string(gray, config="-l kor --psm 7 --oem 1")
print(text)