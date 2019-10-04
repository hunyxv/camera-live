import cv2
import threading
from setting import CAMERA_ID, VIDEO


class CameraFrame(threading.Thread):
    __object = None

    cap = cv2.VideoCapture(CAMERA_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO.get("WIDTH"))   # 480p
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO.get("HEIGHT"))
    cap.set(cv2.CAP_PROP_FPS, VIDEO.get("FPS"))

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    resolution_size = (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )

    def __new__(cls):
        if not cls.__object:
            cls.__object = super().__new__(cls)
        return cls.__object
    
    def __init__(self):
        super().__init__()
        self.result = None

    def run(self):
        self.result = self.cap.read()
    
    def __del__(self):
        self.cap.release()
