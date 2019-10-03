import cv2
import datetime

frontalface_cascade = cv2.CascadeClassifier(
    './cascades/haarcascade_frontalface_default.xml'
)

profileface_cascade = cv2.CascadeClassifier(
    './cascades/haarcascade_profileface.xml'
)

async def frame_processing(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # 正脸
    faces = frontalface_cascade.detectMultiScale(gray, 1.3, 4)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # 左侧脸
    left_faces = profileface_cascade.detectMultiScale(gray, 1.3, 4)
    for (x, y, w, h) in left_faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 右侧脸
    right_flip = cv2.flip(gray, 1)
    right_faces = profileface_cascade.detectMultiScale(right_flip, 1.3, 4)
    for (x, y, w, h) in right_faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # 添加文字
    text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cv2.putText(frame, text, (40, 40), cv2.FONT_HERSHEY_PLAIN, 1.6, (0, 0, 255), 2)

    return frame
    


class VideoProcessing(object):
    def __init__(self, width, height, fps, duration=600):
        self.video_width = width
        self.video_height = height
        self.fps = fps
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.frame_count = 0
        self.video_duration = duration * fps
        self.videofn = None

        self.create_video_fn(self.get1new_vpath())
    
    def create_video_fn(self, video_path):
        self.videofn = cv2.VideoCapture()
        self.videofn.open(video_path, 
            self.fourcc, 
            self.fps, 
            (self.video_width, self.video_height), 
            True
        )

    def get1new_vpath(self):
        """
        create a new video path
        return:
            video_path: string
        """
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=self.video_duration)
        video_name = start_time.strftime('%Y%m%d_%H%M%S') + '-' + end_time.strftime('%Y%m%d_%H%M%S') * '.mp4'
        video_path = './{}/{}/{}'.format(
            '%d%02d' % (start_time.year, start_time.month),
            start_time.day,
            video_name
        )
        return video_path
    
    def record(self, task):
        """
        record videos

        Args:
            task: asyncio task
        """
        frame = task.result()
        
        if self.frame_count > self.video_duration
            self.frame_count = 0
            self.videofn.release()
            new_video_path = self.get1new_vpath()
            self.create_video_fn(new_video_path)
            pass  
            # TODO encrypt and upload to baidu

        self.frame_count += 1
        self.videofn.write(frame)

    def __del__(self):
        self.videofn.release()

