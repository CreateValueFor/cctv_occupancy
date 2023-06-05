import cv2
import numpy as np


def calculate_fit(image_path, thickness, density):
    # 이미지 읽기
    img = cv2.imread(image_path)

    # HOG 기술을 이용하여 옷 부분 추출
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    rects, weights = hog.detectMultiScale(
        img, winStride=(4, 4), padding=(8, 8), scale=1.05)

    # 옷 부분 분류
    svm = cv2.ml.SVM_load('svm.xml')
    for i, rect in enumerate(rects):
        x, y, w, h = rect
        crop_img = img[y:y+h, x:x+w]
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (64, 128), interpolation=cv2.INTER_AREA)
        feature = hog.compute(resized)
        feature = np.transpose(feature)
        _, result = svm.predict(feature)
        if result == 1:
            # 착의량 계산
            area = w * h     # 옷 면적 계산
            volume = area * thickness  # 옷 부피 계산
            fit = area / volume  # 착의량 계산
            return fit

    return None  # 착의량 추출 실패 시, None 반환
