import cv2

from cameraFlow2rtmp import push_flow

rtmp_url = ''

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 704)   # 480p
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 20)

fps = cap.get(cv2.CAP_PROP_FPS)
resolution_size = (
    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
)
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')

flow_pipe = push_flow('x'.join(str(item) for item in resolution_size), fps, rtmp_url)

try:
    success, frame = cap.read() # frame 是一个三维数组 (480, 704, 3) (width, height, RGB)

    while success:
        #frame = cap.retrieve()
        flow_pipe.stdin.write(frame.tostring())
        success, frame = cap.read()

    """
    success = cap.grab()
    while success:
        frame = cap.retrieve()
        flow_pipe.stdin.write(frame[1].tostring())
        success = cap.grab()
    """
except Exception as e:
    print('[ERROR]: {}'.format(e))
finally:
    flow_pipe.stdin.close()
    flow_pipe.kill()
    cap.release()
