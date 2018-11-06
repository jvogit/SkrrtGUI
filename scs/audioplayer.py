import vlc
import time
import subprocess
video_path="sample.mp4"
def PlayVideo(video_path):
    p = vlc.MediaPlayer(video_path)
    p.play()

def LookUpAndPlay(url):
    command=['youtube-dl', 'ytsearch:'+url, '-g']
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True, startupinfo=startupinfo).stdout.split()
    print(str(result[1]))
    PlayVideo(result[1])
