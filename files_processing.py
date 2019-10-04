import os
import cv2
import datetime
import threading



class FrameProcessing(threading.Thread):
    frontalface_cascade = cv2.CascadeClassifier(
        './cascades/haarcascade_frontalface_default.xml'
    )

    profileface_cascade = cv2.CascadeClassifier(
        './cascades/haarcascade_profileface.xml'
    )

    def __init__(self, frame):
        super().__init__()
        self.result = None
        self.frame = frame

    def run(self):
        frame = self.frame
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # 正脸
        faces = self.frontalface_cascade.detectMultiScale(gray, 1.3, 4)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # 左侧脸
        left_faces = self.profileface_cascade.detectMultiScale(gray, 1.3, 4)
        for (x, y, w, h) in left_faces:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # 右侧脸
        right_flip = cv2.flip(gray, 1)
        right_faces = self.profileface_cascade.detectMultiScale(right_flip, 1.3, 4)
        for (x, y, w, h) in right_faces:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        
        # 添加文字
        text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cv2.putText(frame, text, (40, 40), cv2.FONT_HERSHEY_PLAIN, 1.6, (0, 0, 255), 2)
        
        self.result = frame


class VideoProcessing(threading.Thread):
    __object = None
    __has_init = False

    def __new__(cls, frame=None, resolution_size=(0, 0), fps=0, duration=600):
        if not cls.__object:
            cls.__object = super().__new__(cls)
        return cls.__object

    def __init__(self, frame=None, resolution_size=(0, 0), fps=0, duration=600):
        if not VideoProcessing.__has_init:
            self.resolution_size = resolution_size
            self.fps = fps
            self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.frame_count = 0
            self.video_duration = duration * fps
            self.videofn = None

            self.create_video_fn(self.get1new_vpath())
            VideoProcessing.__has_init = True
        super().__init__()
        self.frame = frame
    
    def create_video_fn(self, video_path):
        if not os.path.exists(os.path.dirname(video_path)):
            os.makedirs(os.path.dirname(video_path))

        self.videofn = cv2.VideoWriter()
        self.videofn.open(video_path, 
            self.fourcc, 
            self.fps, 
            self.resolution_size, 
            True
        )

    def get1new_vpath(self):
        """
        create a new video path
        return:
            video_path: string
        """
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=self.video_duration / self.fps)
        video_name = start_time.strftime('%Y%m%d_%H%M%S') + '-' + end_time.strftime('%Y%m%d_%H%M%S') + '.mp4'
        video_path = './{}/{}/{}'.format(
            '%d%02d' % (start_time.year, start_time.month),
            start_time.day,
            video_name
        )
        return video_path
    
    def run(self):
        """
        record videos

        Args:
            task: asyncio task
        """
        if self.frame_count > self.video_duration:
            self.frame_count = 0
            self.videofn.release()
            new_video_path = self.get1new_vpath()
            self.create_video_fn(new_video_path)
            pass  
            # TODO encrypt and upload to baidu

        self.frame_count += 1
        self.videofn.write(self.frame)

    def __del__(self):
        self.videofn.release()

