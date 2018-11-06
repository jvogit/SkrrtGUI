import vlc
import time
import subprocess
video_path="sample.mp4"
def PlayVideo(video_path, blocking=False):
    p = vlc.MediaPlayer(video_path)
    p.play()
    if blocking:
        while 1:
            if p.is_playing():
                break

def LookUpAndPlay(url, video=False, tts=None):
    command=['youtube-dl', 'ytsearch:'+url, '-g', '-e']
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True, startupinfo=startupinfo).stdout.split('\n')
    print(str(result))
    if tts is not None:
        tts('Now playing:' + result[0])
    if video:
        PlayVideo(result[1], True)
    PlayVideo(result[2])
