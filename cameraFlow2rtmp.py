import subprocess
import shlex

from urllib import parse
from setting import RTMP, VIDEO

class FFPushFlow(object):
    def __init__(self, resolution_size, fps):
        self.rtmp_url = RTMP.get('RTMP_ADDR') + '?' + parse.urlencode(RTMP.get('payload'))
        self.resolution_size = resolution_size
        self.fps = fps

        self.ffp = self.create_live_flow()

    def create_live_flow(self):
        """
        Args：
            resolution: image or video resolution rate
            fps：video fps
            rtmp_url: rtmp service addr
        Return:
            subprocess.PIPE  stdin
        """
        command = "ffmpeg -y -f rawvideo -pix_fmt bgr24 -s {resolution} -r {fps} -i - -c:v libx264 -pix_fmt yuv420p -preset ultrafast -f flv {rtmp_url}".format(
            resolution=self.resolution_size, 
            fps=self.fps, 
            rtmp_url=self.rtmp_url
        )
        """
        -f rawvideo： 将输入格式设置为原始视频容器
        -pix_fmt: 像素格式，opencv 默认的像素格式 是 bgr，后面将 bgr 转为 yuyv 格式
        -preset h.264 压缩速度选择， ultrafast 是最快的 更多看：https://trac.ffmpeg.org/wiki/Encode/H.264
        """
        ffp = subprocess.Popen(
            shlex.split(command), stdin=subprocess.PIPE
        )
        return ffp
    
    def push_flow(self, task):
        frame = task.result()
        self.ffp.stdin.write(frame.tostring())

    def pid(self):
        return self.ffp.pid
    
    def kill(self):
        try:
            self.ffp.send_signal(9)
        except Exception as e:
            print(e)
            self.ffp.kill()

    def is_alive(self):
        if not self.ffp.poll():
            return True
        else:
            return False

    def restart(self):
        self.ffp.stdin.close()
        self.kill()

        self.ffp = self.create_live_flow()



    def __del__(self):
        self.ffp.stdin.close()
        self.kill()
