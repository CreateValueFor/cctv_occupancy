# https://pysource.com/2023/03/28/object-detection-with-yolo-v8-on-mac-m1-opencv-with-python-tutorial
import cv2
from ultralytics import YOLO
import numpy as np
import time
import os
import common
import OCR
import opencv
import pytesseract
import re

pattern = r"\d|:"
pattern2 = r"(?:\d{2}:){3}\d{2}"
# titlePattern = r"\d+_|_\d+|\d+"
titlePattern = r"\d+"


pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# path = "/Volumes/college/video/"

# file_list = os.listdir(path)
file_list = ['cafe.mp4']
log_path = "./logs/"
model = YOLO("yolov8m.pt")

if __name__ == "__main__":

    for video in file_list:
        if (video[0] == "."):
            continue
        print(video)

        # cap = cv2.VideoCapture(path + video)
        test_text = "MAIN-학술정보관 1-학술정보관 1층 로비3-Video-20230420_183018_01.mp4.csv"
        cap = cv2.VideoCapture(video)
        logname = "".join(re.findall(titlePattern, test_text)[3])
        csv = open(log_path + logname + ".csv", 'w')
        csv.write("Time,Occupancy" + '\n')

        while True:
            for _ in range(0, 5):
                cap.grab()
            ret, frame = cap.read()
            if not ret:
                break

            # 이미지 clip
            x, y, w, h = int(frame.shape[1] * 0.425), int(frame.shape[0] * 0.9), int(
                frame.shape[1] * 0.14), int(frame.shape[0] * 0.1)
            clip_img = frame[y:y+h, x:x+w]

            # # clip 된 이미지 전처리
            # gray = cv2.cvtColor(clip_img, cv2.COLOR_BGR2GRAY)

            # # 이진화
            # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

            # 추출된 이미지에 사각형 그리기
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # 이미지에서 텍스트 추출
            text = pytesseract.image_to_string(clip_img, lang='eng')
            date = "".join(re.findall(pattern2, text))

            # 추출된 프레임 화면에 표시
            cv2.putText(frame, date, (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # cv2.imshow("Frame", frame)

            # gray = cv2.cvtColor(clip_img, cv2.COLOR_BGR2GRAY)

            # cv2.imshow("Frame", frame)

            # textArea = OCR.clipText(frame)
            # text = OCR.contractText(textArea)
            # continue

            results = model(frame, device="mps")
            result = results[0]
            bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
            classes = np.array(result.boxes.cls.cpu(), dtype="int")

            # opencv.drawPerson(classes, bboxes, frame)

            count = common.count_zeros(classes)
            cv2.putText(frame, "people count: {}".format(count), (x, y-30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            csv.write("{} {}".format(logname, date) + ", " + str(count) + '\n')

            cv2.imshow("Img", frame)
            if cv2.waitKey(1) == ord('q'):
                break
        csv.flush()
        csv.close()
        cap.release()
        cv2.destroyAllWindows()
