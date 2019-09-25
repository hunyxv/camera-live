import cv2
import asyncio
from setting import CAMERA_ID, VIDEO
from cameraFlow2rtmp import FFPushFlow
from files_processing import frame_processing, VideoProcessing

cap = cv2.VideoCapture(CAMERA_ID)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO.get("WIDTH"))   # 480p
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO.get("HEIGHT"))
cap.set(cv2.CAP_PROP_FPS, VIDEO.get("FPS")) 

fps = cap.get(cv2.CAP_PROP_FPS)
resolution_size = (
    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
)

ffmpeg_push_flow = FFPushFlow(resolution_size, fps)
video_processing = VideoProcessing(
    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), 
    fps, Video.get("DURATION")
)

async def run():
    try:
        success, frame = cap.read()
        while success:
            task1 = asyncio.create_task(frame_processing(frame))
            task2 = asyncio.create_task(cap.read())

            task1.add_done_callback(ffmpeg_push_flow.push_flow)
            task1.add_done_callback(video_processing.record)

            await task1
            success, frame = await task2
    except Exception as e:
        print(e)
    finally:
        cap.release()