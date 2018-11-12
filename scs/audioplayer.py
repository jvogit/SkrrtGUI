import vlc
import time
import subprocess
video_path="sample.mp4"
class AudioPlayer():
    def __init__(self):
        self.p = None
        self.a = None
    def PlayVideo(self, video_path, blocking=False):
        if self.p is not None:
            self.p.stop()
        self.p = vlc.MediaPlayer(video_path)
        self.p.play()
        if blocking:
            while 1:
                if self.p.is_playing():
                    break
    def PlayAudio(self, video_path, blocking=False):
        if self.a is not None:
            self.a.stop()
        self.a = vlc.MediaPlayer(video_path)
        self.a.play()
        if blocking:
            while 1:
                if self.a.is_playing():
                    break
    def inde_play(self, path):
        vlc.MediaPlayer(path).play()
        
    def stop(self):
        if self.a is not None:
            self.a.stop()
        if self.p is not None:
            self.p.stop()
            
    def pause(self):
        if self.a is not None:
            self.a.pause()
        if self.p is not None:
            self.p.pause()

    def LookUpAndPlay(self, url, video=False, tts=None):
        command=['youtube-dl', 'ytsearch:'+url, '-g', '-e']
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True, startupinfo=startupinfo).stdout.split('\n')
        print(str(result))
        self.pause()
        if video:
            self.PlayVideo(result[1], True)
        self.PlayAudio(result[2])
        if tts is not None:
            tts('Now playing:' + result[0])
