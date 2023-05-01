import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'


def clipText(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 글자 영역 필터링
    max_area = 0
    best_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        if area > max_area and y + h > img.shape[0] * 0.9:  # 이미지의 하단 부분에서 찾기
            max_area = area
            best_cnt = cnt

    # 글자 영역 추출
    if best_cnt is not None:
        x, y, w, h = cv2.boundingRect(best_cnt)
        character_img = img[y:y+h, x:x+w]
        return character_img


def contractText(img):

    text = pytesseract.image_to_string(img)
    return text
