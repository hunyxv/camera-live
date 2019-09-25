import cv2
import datetime

async def frame_processing(frame):
    pass

class VideoProcessing(object):
    def __init__(self, width, height, fps, duration=600):
        self.video_width = width
        self.video_height = height
        self.fps = fps
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.fps_count = 0
        self.video_duration = duration
        self.videofn = None
    
    def create_video_fn(self, video_path):
        if self.videofn:
            self.videofn.release()

        self.videofn = cv2.VideoCapture()
        self.videofn.open(video_path, 
            self.fourcc, 
            self.fps, 
            (self.video_width, self.video_height), 
            True
        )

    def get1new_vpath(self):
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=self.video_duration)
        video_name = start_time.strftime('%Y%m%d_%H%M%S') + '-' + end_time.strftime('%Y%m%d_%H%M%S')
        video_path = './{}/{}/{}'.format(
            '%d%02d' % (start_time.year, start_time.month),
            start_time.day,
            video_name
        )
        return video_path
    
    def record(self, task):
        self.fps_count += 1
        frame = task.result()
        
        if self.fps_count > self.video_duration * self.fps:
            self.fps_count = 1
            new_video_path = self.get1new_vpath()
            self.create_video_fn(new_video_path)
            pass  # do something save video file
        
        self.videofn.write(frame)

    def __del__(self):
        self.videofn.release()

