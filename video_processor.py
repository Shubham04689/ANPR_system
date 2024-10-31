import cv2
from datetime import datetime

class VideoProcessor:
    def __init__(self, source):
        self.source = source
        self.cap = cv2.VideoCapture(source)

    def process(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield frame, timestamp

    def __del__(self):
        self.cap.release()