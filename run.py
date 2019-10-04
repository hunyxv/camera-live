# 守护进程 https://www.cnblogs.com/robinunix/p/8436455.html#_label0
# 原文： https://blog.csdn.net/tao_627/article/details/49532021
from camera_data_read import CameraFrame
from cameraFlow2rtmp import FFPushFlow
from files_processing import FrameProcessing, VideoProcessing
from cameraFlow2rtmp import FFPushFlow
from setting import VIDEO

ffmpeg_push_flow = FFPushFlow(
    resolution_size=CameraFrame.resolution_size,
    fps=CameraFrame.fps
)

video_processing = VideoProcessing(
    resolution_size=CameraFrame.resolution_size,
    fps=CameraFrame.fps, duration=VIDEO.get("DURATION")
)

def start_join(tasks=[]):
    for task in tasks:
        task.start()

    for task in tasks:
        task.join()

def main():
    t_cap = CameraFrame()
    start_join([t_cap])
    success, frame = t_cap.result
    
    while success:
        t_frame = FrameProcessing(frame)
        t_cap = CameraFrame()
        start_join([t_frame, t_cap])

        new_frame = t_frame.result
        t_video = VideoProcessing(frame=new_frame)
        t_plow = FFPushFlow(frame=new_frame)
        start_join([t_video, t_plow])

        success, frame = t_cap.result


if __name__ == "__main__":
    main()