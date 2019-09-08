import subprocess
import shlex

def push_flow(resolution, fps, rtmp_url=None):
    """
    Args：
        resolution: image or video resolution rate
        fps：video fps
        rtmp_url: rtmp service addr
    Return:
        subprocess.PIPE  stdin
    """
    command = "ffmpeg -y -f rawvideo -pix_fmt bgr24 -s {resolution} -r {fps} -i - -c:v libx264 -pix_fmt yuv420p -preset ultrafast -f flv {rtmp_url}".format(
        resolution=resolution, fps=fps, rtmp_url=rtmp_url
    )
    """
    -f rawvideo： 将输入格式设置为原始视频容器
    -pix_fmt: 像素格式，opencv 默认的像素格式 是 bgr，后面将 bgr 转为 yuyv 格式
    -preset h.264 压缩速度选择， ultrafast 是最快的 更多看：https://trac.ffmpeg.org/wiki/Encode/H.264
    """
    input_pipe = subprocess.Popen(
        shlex.split(command), stdin=subprocess.PIPE
    )
    return input_pipe
