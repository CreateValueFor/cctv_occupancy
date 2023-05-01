import cv2


def drawPerson(classes, bboxes, image):
    for cls, bbox in zip(classes, bboxes):
        if (cls == 0):
            (x, y, x2, y2) = bbox
            cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 225), 2)
            cv2.putText(image, str(cls), (x, y - 5),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 225), 2)
